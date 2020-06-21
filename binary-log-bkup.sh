#!/bin/bash

/usr/local/mysql/bin/mysqladmin -p flush-logs

binlog_nm=`tail -2 /usr/local/mysql/data/mysql-bin.index | head -n 1 | awk '{ print substr($1,3)}'`

bkup_nm=`/usr/local/mysql/bin/mysql -p -A admin -e "select bk_name from backup_history order by id desc limit 1"`

/usr/local/mysql/bin/mysql -p -A admin -e "insert into binary_logs (binlog_nm, bkup_nm) values ('$binlog_nm','$bkup_nm')"

cp /usr/local/mysql/data/$binlog_nm "/Volumes/Time Machine Backup/mysql-backup/binlogs"
