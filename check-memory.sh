#!/bin/bash

###################################################
## Script to check and see how much memory	 ##
## that MySQL is using.				 ##
## Updates the memory_usage table in the admin   ##
## database.                                     ##
###################################################
## Written By: Wayne Leutwyler                   ##
## Date: 2/20/2013                               ##
###################################################

USER="mysqlagent"
PASSWD=`cat /home/mysqladm/data/rose-lab1.txt`
HOST="rose-lab1"
DB="admin"

ps acux | grep mysqld | grep -v mysqld_safe | awk '{print "insert into memory_usage (pcttolmemused,VirtMem,RealMem) values ("$4","$5/1024","$6/1024");"}' | /home/mysqladm/mysql/bin/mysql -u $USER -p$PASSWD -h $HOST $DB 2>/dev/null
