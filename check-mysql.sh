#!/bin/bash

##################################################
## Script to check and see if mysql is running. ##
## If mysql is NOT running this script will     ##
## start the mysql server and send e-mail to    ##
## the DBA team.                                ##
##################################################
## Written By: Wayne Leutwyler                  ##
## Date: 1/30/2013                              ##
##################################################

DATE=`date +%Y%m%d`
TIME=`date +%H%M`
LOGFILE="/home/mysqladm/log/check-mysql.$DATE.$TIME.log"
pidfile=/home/mysqladm/tmp/mysqld.pid
stoppedfile=/home/mysqladm/data/stopped
EMAIL_LIST=""

#Remove logs older than 21 days
find /home/mysqladm/log/check-mysql* -mtime +21 -exec rm {} \; 2>/dev/null

# Check for stopped file, if present exit script.
if [[ -e $stoppedfile ]]
	then
	exit
fi

if [[ -e $pidfile ]]
	then
	exit
	#No longer logging success. 03/15/2013
	#echo "$HOSTNAME MySQL Server is running."
	else
	echo "MySQL - WARNING: $HOSTNAME MySQL Server is not running, starting it now." > $LOGFILE
	echo " " >> $LOGFILE
	echo "Inspect /home/mysqladm/mysql/log/mysqld.log for more details." >> $LOGFILE
	mail -s "MySQL - Warning: Ubuntu-Desktop MySQL Server Down" $EMAIL_LIST < $LOGFILE
	/home/mysqladm/mysql/mysql.server start

#Sleep for 60 seconds to allow server to restart.
sleep 60

# Verify that MySQL restarted, send e-mail with results
	if [[ -e $pidfile ]]
		then
		echo "MySQL - RECOVERY: $HOSTNAME MySQL Server is UP." > $LOGFILE
		echo " " >> $LOGFILE
		echo "Inspect /home/mysqladm/mysql/log/mysqld.log for more details." >> $LOGFILE
		mail -s "MySQL - RECOVERY: Ubuntu-Desktop MySQL Server is UP." $EMAIL_LIST < $LOGFILE
		else
		echo "MySQL - Critical: $HOSTNAME MySQL Server did not re-start on the second attempt." > $LOGFILE
		echo " " >> $LOGFILE
		echo "Inspect /home/mysqladm/mysql/log/mysqld.log for more details." >> $LOGFILE
		mail -s "MySQL - Critical: Ubuntu-Desktop MySQL Server did not restart." $EMAIL_LIST < $LOGFILE
	fi
fi
