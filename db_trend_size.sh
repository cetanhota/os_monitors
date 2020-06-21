FILE='/home/mysqladm/data/trend-size.txt'
 
if [[ -e $FILE ]] ; then
        rm $FILE
fi
 
for SERVER in `cat /home/mysqladm/data/serverlist` ;    do
 
DF_OUT=`ssh $SERVER df | grep / | grep -vE '/dev/sda1|nfs_share|tmpfs|/dev/mapper/VolGroup-lv_root'`
FL_ALLOC_SZ=`echo $DF_OUT | awk '{ print $1 }'`
FL_USED_SZ=`echo $DF_OUT | awk '{ print $2 }'`
FL_USED_PER=`echo $DF_OUT | awk '{ print $4 }'`
 
echo $SERVER,$FL_ALLOC_SZ,$FL_USED_SZ,$FL_USED_PER >> $FILE
done
 
/home/mysqladm/mysql/bin/mysql admin -e "load data infile '$FILE' into table db_trend_size FIELDS TERMINATED BY
',' (server_name,fl_alloc_sz_kb,fl_used_sz_kb,fl_used_per);"

if [[ -e $FILE ]] ;  then
rm $FILE
fi
