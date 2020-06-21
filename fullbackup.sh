#/bin/bash

##### OLD Backup, not being used. #####
#/usr/local/mysql/bin/mysqldump -phawk69 -A -F --single-transaction  --master-data=2 > "/Volumes/Time Machine Backup/mysql-backup/full-backup_$(/bin/date +%m%d%y%H%M).sql"

/usr/local/mysql/bin/mysql -u  -p -e "flush tables with read lock"
/usr/local/mysql/bin/mysql -u  -p -e "flush logs"

tar zcvvf "/media/sf_BACKUP/fullbackup_$(/bin/date +%m%d%y%H%M).tar.gz" /usr/local/mysql/data/*

/usr/local/mysql/bin/mysql -u  -p -e "unlock tables"

bkup=`ls -latr "/media/sf_BACKUP" | tail -1 | awk '{print $9}'`

binlog=`tail -1 /usr/local/mysql/binlog/mysql-bin.index | awk '{ print substr($1,29)}'`

/usr/local/mysql/bin/mysql -u  -p -A admin -e "insert into backup_history (server_name,location,bk_type,bk_name,binary_log) values ('$HOSTNAME','/media/sf_BACKUP','Full','$bkup','$binlog')"
