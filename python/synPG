import psycopg2
import logging
from datetime import datetime

def sync_database_structure(src_db_config, dst_db_configs):
    conn_src = psycopg2.connect(
        dbname=src_db_config["dbname"],
        user=src_db_config["user"],
        password=src_db_config["password"],
        host=src_db_config["host"],
        port=src_db_config["port"]
    )

    logging.info(f"源数据库：{src_db_config}")

    src_cursor = conn_src.cursor()

    src_cursor.execute(
        ("SELECT table_name, column_name, udt_name,character_maximum_length,numeric_precision,numeric_scale,is_nullable "
         "FROM information_schema.columns "
         "WHERE table_schema = 'public' order by table_name,ordinal_position"))
    src_tables = src_cursor.fetchall()


    src_cursor.execute("SELECT c.relname AS table_name, d.description AS table_comment FROM pg_class c "
                       "LEFT JOIN pg_description d ON d.objoid = c.oid "
                       "WHERE c.relkind = 'r' AND d.description IS NOT NULL AND d.objsubid = 0 ORDER BY c.relname")
    src_tables_desc = src_cursor.fetchall()


    src_cursor.execute("SELECT c.relname AS table_name, a.attname AS column_name, d.description AS column_comment FROM pg_attribute a "
                       "JOIN pg_class c ON c.oid = a.attrelid "
                       "JOIN pg_namespace n ON n.oid = c.relnamespace "
                       "LEFT JOIN pg_description d ON d.objoid = a.attrelid AND d.objsubid = a.attnum "
                       "WHERE a.attnum > 0 AND NOT a.attisdropped AND d.description IS NOT NULL AND c.relkind = 'r' ORDER BY n.nspname, c.relname, a.attname")
    src_columns_desc = src_cursor.fetchall()


    src_cursor.execute("SELECT kcu.table_name, kcu.column_name, kcu.constraint_name FROM information_schema.table_constraints AS tc "
                       "JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name WHERE tc.constraint_type = 'PRIMARY KEY'")
    src_primary_keys = src_cursor.fetchall()
    

    dst_db_configs = ensure_list(dst_db_configs)
    for dst_db_config in dst_db_configs:
        conn_dst = psycopg2.connect(
        dbname=dst_db_config["dbname"],
        user=dst_db_config["user"],
        password=dst_db_config["password"],
        host=dst_db_config["host"],
        port=dst_db_config["port"]
    )
        logging.info(f"目标数据库: {dst_db_config}")
        dst_cursor = conn_dst.cursor()
        dst_cursor.execute(
            ("SELECT table_name, column_name, udt_name,character_maximum_length,numeric_precision,numeric_scale,is_nullable "
             "FROM information_schema.columns "
             "WHERE table_schema = 'public' order by table_name,ordinal_position"))
        dst_tables = dst_cursor.fetchall()

        dst_cursor.execute(
            "SELECT kcu.table_name, kcu.column_name, kcu.constraint_name FROM information_schema.table_constraints AS tc "
            "JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name WHERE tc.constraint_type = 'PRIMARY KEY'")
        dst_primary_keys = dst_cursor.fetchall()


        for src_table in src_tables:
            table_name, column_name, data_type, length, start, end, is_nullable = src_table

            src_table_desc = next((t for t in src_tables_desc if t[0] == table_name), None)
            src_column_desc = next((t for t in src_columns_desc if t[0] == table_name and t[1] == column_name), None)

            data_type_value = trans_data_type(data_type, length, start, end)

            if is_nullable == "NO":
                data_type_value += " NOT NULL"

            dst_table = next((t for t in dst_tables if t[0] == table_name), None)
            if dst_table is None:
                dst_tables.append((table_name, column_name, data_type, length, start, end, is_nullable))
                dst_cursor.execute(f"create table {table_name} ({column_name} {data_type_value} )")
                if src_table_desc is not None:
                    dst_cursor.execute(f"comment on table {table_name} is '{src_table_desc[1]}'")
                if src_column_desc is not None:
                    dst_cursor.execute(f"comment on column {table_name}.{column_name} is '{src_column_desc[2]}'")
                continue

            dst_table2 = next((t for t in dst_tables if t[0] == table_name and t[1] == column_name), None)
            if dst_table2 is None:
                dst_cursor.execute(f"alter table {table_name} add column {column_name} {data_type_value}")

                if src_column_desc is not None:
                    dst_cursor.execute(f"comment on column {table_name}.{column_name} is '{src_column_desc[2]}'")
                continue


            dst_table3 = next((t for t in dst_tables if t[0] == table_name and t[1] == column_name and t[2] == data_type and t[3] == length and t[4] == start and t[5] == end and t[6] == is_nullable),None)
            try:
                if dst_table3 is None:
                    if is_nullable == "NO":
                        data_type_value = data_type_value.replace('NOT NULL', '')
                        dst_cursor.execute(f"alter table {table_name} alter column {column_name} set not null")
                    dst_cursor.execute(f"alter table {table_name} alter column {column_name} type {data_type_value}")

                    if src_column_desc is not None:
                        dst_cursor.execute(f"comment on column {table_name}.{column_name} is '{src_column_desc[2]}'")
            except Exception as e:
                logging.error(e)

        for src_primary_key in src_primary_keys:
            table_name, column_name, constraint_name = src_primary_key

            src_key = next((t for t in dst_primary_keys if t[0] == table_name), None)
            if src_key is None:
                try:
                    dst_cursor.execute(f"alter table {table_name} add constraint {constraint_name} primary key ({column_name}) ")
                except Exception as e:
                    logging.error(f"alter table {table_name} add constraint {constraint_name} primary key ({column_name}) ")
                    logging.error(e)
                continue

            src_key = next((t for t in dst_primary_keys if t[0] == table_name and t[1] == column_name and t[2] == constraint_name), None)
            if src_key is None:
                try:
                    dst_cursor.execute(f"alter table {table_name} drop constraint {constraint_name}")
                    dst_cursor.execute(
                        f"alter table {table_name} add constraint {constraint_name} primary key ({column_name}) ")
                except Exception as e:
                    logging.error(e)

        conn_dst.commit()
        conn_dst.close()
        logging.info(f"同步完成:{dst_db_config} 与 {src_db_config} ")

    conn_src.close()


def trans_data_type(data_type, length, start, end) -> str:
    value=None
    if length is not None:
        value = f"{data_type}({length})"
    if length is None and start is None and end is None:
        value = f"{data_type}"
    if length is None and start is not None and (data_type in ("numeric","decimal") or data_type.startswith("float")):
        value = f"{data_type}({start},{end})"
    if length is None and start is not None and data_type.startswith("int"):
        value = f"{data_type}"

    return value

def ensure_list(x):
    if not isinstance(x, list):
        return [x]
    return x


if __name__ == '__main__':

    #pyinstaller --onefile --name mes-pg .\syncPG.py


    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"pg_sync_{current_time}.log"
    logging.basicConfig(filename=log_filename, level=logging.INFO)

    src_db_config = {
        "dbname": "source",
        "user": "postgres",
        "password": "pwd",
        "host": "192.168.110.54",
        "port": "5434"}

    dst_db_configs = [{"dbname": "target1", "user": "postgres", "password": "pwd", "host": "192.168.110.54",
                       "port": "5434"},
                      {"dbname": "target2", "user": "postgres", "password": "pwd", "host": "192.168.110.54",
                       "port": "5434"}]

    sync_database_structure(src_db_config, dst_db_configs)

