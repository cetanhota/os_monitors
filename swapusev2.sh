#!/bin/bash
#Script By Wayne Leutwyler
#12/15/2016
# Script will collect swap use, and output to csv.

path=filebeat
cd $HOME/$path 
rm $HOME/$path/csv/swapuse.csv
export sesDate=`date +'%m-%d-%Y %H:%M:%S'`
free | tail -n 1 | awk '{printf("%s,%s,%s,%s\n",ENVIRON["sesDate"],$2,$3,$4)}' > csv/swapuse.csv
