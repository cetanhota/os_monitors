#!/bin/bash
#Script By Wayne Leutwyler
#12/15/2016
# Script will collect top 5 cpu users, and output to csv.

path=filebeat
cd $HOME/$path
rm $HOME/$path/csv/top5cpu.csv
export sesDate=`date +'%m-%d-%Y %H:%M:%S'`
top -b -n 1 | head -n 12  | tail -n 5 | awk '{printf("%s,%s,%s,%s\n",ENVIRON["sesDate"],$2,$9,$12)}' > csv/top5cpu.csv
