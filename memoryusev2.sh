#!/bin/bash
#Script By Wayne Leutwyler
#12/15/2016
# Script will collect memory usage, and output to csv.

export sesDate=`date +'%m-%d-%Y %H:%M:%S'`
path=filebeat
cd $HOME/$path
rm $HOME/$path/csv/memoryuse.csv
free | tail -n 2 | head -n 1 | awk '{printf("%s,%s,%s\n",ENVIRON["sesDate"],$3,$4)}' > csv/memoryuse.csv
