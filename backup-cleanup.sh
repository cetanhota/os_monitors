#!/bin/bash
###################################################
## Find and remove all files older than 30 days. ##
###################################################
/usr/bin/find /media/BACKUP -mtime +10 -exec rm {} \;
