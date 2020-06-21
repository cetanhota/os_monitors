#!/bin/bash

###################################################
## Script to check and see max user connections	 ##
## that MySQL is using.				 ##
##						 ##
##						 ##
###################################################
## Written By: Wayne Leutwyler                   ##
## Date: 2/28/2013                               ##
###################################################

USER="mysqlagent"
PASSWD=`cat /home/mysqladm/data/rose-lab1.txt`
HOST="rose-lab1"
DB="information_schema"
DATE=`date +%Y%m%d`
TIME=`date +%H%M`
LOGFILE="/home/mysqladm/log/check-max-connections.$DATE.$TIME.log"
CONN=`mysql --skip-column-names -u $USER -p$PASSWD -h $HOST $DB -e "select (variable_value/@@max_connections) as '% Max Connections Used' from global_status where variable_name='Threads_connected'"`

echo $CONN > $LOGFILE

if [[ $CONN > 0.85 ]];
	then
	mail -s "WARNING = $HOST Connections greater than 85%" wayne.leutwyler@gmail.com < $LOGFILE
fi
