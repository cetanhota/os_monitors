#!/bin/bash

PATH="$HOME/bin:/home/mysqladm/mysql/bin:/home/mysqladm/backup/bin:$PATH"
PASSWD=`cat /home/mysqladm/data/rose-lab1.txt`

### Clean up all backups and log files ###
#find /home/mysqladm/log/full-database-backup* -mtime +5 -exec rm {} \; 2>/dev/null
#find /mysbackup/full/* -mtime +5 -exec rm -f -R {} \; 2>/dev/null

### Full backup of databases ###
innobackupex --stream=xbstream /media/sf_vm-share/full-backup --defaults-file=/home/mysqladm/mysql/my.cnf --user=mysqladm --password=hawk69 --socket=/home/mysqladm/tmp/mysql.sock --no-lock --extra-lsndir=/tmp --no-timestamp > /media/sf_vm-share/full-backup/rose-lab1.xbs

echo
echo "##########################"
echo "##### BACKUP COMPLETE ####"
echo "##########################"

#backup=`ls -latr /mysbackup/full | tail -1 | awk '{print $9}'`

### Prepare full backup ###
#/home/mysqladm/backup/bin/innobackupex --user=mysqladm --password=$PASSWD --defaults-file=/home/mysqladm/mysql/my.cnf --apply-log /mysbackup/full/$backup
#echo
#echo "##################################"
#echo "##### BACKUP PREPARE COMPLETE ####"
#echo "##################################"

#binlog=`tail -1 /home/mysqladm/mysql/binlog/mysql-bin.index | awk '{ print substr($1,29)}'`

### Insert data into history table ###
#/home/mysqladm/mysql/bin/mysql -u mysqladm -p$PASSWD -h ubuntu-desktop -A admin -e "insert into backup_history (server_name,location,bk_type,bk_name,binary_log) values ('$HOSTNAME','/mysbackup/full','Full','$backup','$binlog')"

