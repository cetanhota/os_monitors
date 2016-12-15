#!/bin/bash
#Script By Wayne Leutwyler
#12/15/2016
# Script will collect load avg, and output to csv.

path=filebeat
cd $HOME/$path
rm $HOME/filebeat/csv/loadavg.csv
export sesDate=`date +'%m-%d-%Y %H:%M:%S'`
top -b -n 1 | head -n 1 | awk '{printf("%s,%s%s%s\n",ENVIRON["sesDate"],$11,$12,$13)}' > csv/loadavg.csv
