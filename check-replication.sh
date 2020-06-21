#!/bin/bash

###################################################
## Script to check and see if mysql replications ##
## is running. If mysql replication is NOT	 ##
## running this script will send e-mail to the   ##
## DBA team.                                     ##
###################################################
## Written By: Wayne Leutwyler                   ##
## Date: 2/08/2013                               ##
###################################################

# Clean up replication logs older than 21 days
find /home/mysqladm/log/ -name "check-replication*" -mtime +21 -exec rm {} \; 2>/dev/null

USER="mysqlagent"
PASSWD=`cat /home/mysqladm/data/rose-lab2.txt`
HOST="192.168.1.22"
DATE=`date +%Y%m%d`
TIME=`date +%H%M`
LOGFILE="/home/mysqladm/log/check-replication.$DATE.$TIME.log"
CHECKFILE="/home/mysqladm/data/check"
EMAIL_LIST=""

### Get host name of server ###
mysql -u $USER -p$PASSWD -h $HOST -e "select variable_value as 'Host Name:' from information_schema.global_variables where variable_name = 'hostname'" 2>&1 > $LOGFILE
echo " " >> $LOGFILE

### Check replication status and wait 60 seconds. ###
(echo -e "show slave status \G;") | mysql -u $USER -p$PASSWD -h $HOST 2>&1 | grep "Slave_.*_Running: No" > $CHECKFILE
if [ "$?" -ne "1" ]; then
	sleep 60
	rm $CHECKFILE
fi

### Check replication for 2nd time, send mail if down. ###
(echo -e "show slave status \G;") | mysql -u $USER -p$PASSWD -h $HOST 2>&1 | grep "Slave_.*_Running: No" >> $LOGFILE
if [ "$?" -ne "1" ]; then
	echo -e "\nReplication is DOWN. Logon to $HOST and check the slave status." >> $LOGFILE
	mail -s "WARNING = $HOST Replication DOWN" $EMAIL_LIST < $LOGFILE
	else
	# No longer logging success 03/15/2013
	# echo "$HOST Repication is UP" > $LOGFILE
	# Removing all log files if replication is up.
	rm $CHECKFILE
	rm $LOGFILE
fi
