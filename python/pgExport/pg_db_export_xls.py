import socket

import psycopg2
import socks
from docx import Document
import pandas as pd
from openpyxl import load_workbook

def sync_database_structure():
    conn_src = psycopg2.connect(
        dbname="devdb",
        user="pg",
        password="pwd",
        port="58378",
        host="127.0.0.1"
    )

    sel_table_info = conn_src.cursor()
    sel_table_info.execute("SELECT ns.nspname AS table_schema, col.table_name, col.column_name, col.data_type,"
                           " CASE WHEN col.character_maximum_length IS NOT NULL THEN col.character_maximum_length::text "
                           "WHEN col.numeric_precision IS NOT NULL THEN col.numeric_precision::text ELSE '' END AS column_length, "
                           "CASE WHEN col.is_nullable = 'NO' THEN '是' ELSE '否' END AS required_field, obj_description(cls.oid, 'pg_class') AS table_comment, "
                           "col_description(cls.oid, col.ordinal_position::int) AS column_comment "
                           "FROM information_schema.columns col JOIN pg_class cls ON cls.relname = col.table_name JOIN pg_namespace ns "
                           "ON ns.oid = cls.relnamespace WHERE ns.nspname = 'safecommon' AND col.table_name LIKE 'sf_%' "
                           "ORDER BY col.table_name, col.ordinal_position")

    writer_info = pd.ExcelWriter('table.xlsx')
    result = []

    sel_table_infos = sel_table_info.fetchall()
    for sel_table_info in sel_table_infos:
        table_schema = sel_table_info[0]
        table_name = sel_table_info[1]
        table_desc = sel_table_info[6]
        col_name = sel_table_info[2]
        col_data_type = sel_table_info[3]
        col_length = sel_table_info[4]
        col_required_field = sel_table_info[5]
        col_description = sel_table_info[7]

        result.append([table_desc if table_desc else ""])
        result[-1].append(table_name)
        result[-1].append(col_description if col_description else "")
        result[-1].append(col_name)

        if col_data_type == 'USER-DEFINED':
            col_data_type = 'datetime'
        elif col_length:
            col_data_type = f'{col_data_type}({col_length})'

        result[-1].append(col_data_type)
        result[-1].append( '/')
        result[-1].append(col_required_field)
        result[-1].append('')
        result[-1].append('')
        result[-1].append('/')

    df = pd.DataFrame(result)
    df.to_excel('table.xlsx')

    wb = load_workbook('table.xlsx')

    # 保存文档
    wb.save('table.xlsx')
    conn_src.close()


if __name__ == '__main__':

    sync_database_structure()