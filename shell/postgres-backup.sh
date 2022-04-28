#!/bin/sh

echo "============ backup postgres================"
cd /root/postgres
FILE=bk-all-$(date +%Y%m%d%H%M%S).dump
docker exec -e PGUSER=postgres -e PGPASSWORD=111111 root_postgres_1 pg_dumpall -c >$FILE
tar -zcvf $FILE.tar.gz $FILE
rm -f $FILE
mv $FILE.tar.gz /root/backup/


echo "======== del docker run logs ========"
logs=$(find /var/lib/docker/containers/ -name *-json.log)

for log in $logs
        do
                echo "clean logs : $log"
                cat /dev/null > $log
        done


echo "============ del 5days logs============="
find /root/ -mtime +5 -name *.log  -exec rm -f {} \;


:<<!
postgres还原
docker exec -it -e PGUSER=postgres -e PGPASSWORD=111111 root_postgres_1 \
psql -f /var/lib/postgresql/data/all-2022091609091631757366.bak postgres

挂载windows目录
mount -t cifs -o username=administrator,password='123456',gid='0',uid='0' //192.168.1.100/backup /root/backup
echo "//192.168.1.100/postgre-backup /home/ps/backup2 cifs username=administrator,password=123456,gid=0,uid=0,auto 0 0 " >>/etc/fstab

!