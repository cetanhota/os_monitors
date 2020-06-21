#!/bin/bash

URL=$1
KEY=$2
CRIT=$3
http_proxy=""

DEBUG=

if [ -z $CRIT ]; then
   echo "Usage $0 <url> <keyword> <timeout>"
   exit 3
fi

TC=`echo ${URL} | awk -F. '{print \$1}' |awk -F/ '{print \$NF}'`
TMP="/tmp/check_http_sh_${TC}.tmp"

CMD_TIME="curl -k --location --no-buffer --silent --output ${TMP} -w %{time_connect}:%{time_starttransfer}:%{time_total} '${URL}'"
TIME=`eval $CMD_TIME`

if [ -f $TMP ]; then
   RESULT=`grep -c $KEY $TMP`
else
   echo "UNKOWN - Could not create tmp file $TMP"
#   exit 3
fi

TIMETOT=`echo $TIME | gawk  -F: '{ print \$3 }'`

if [ ! -z $DEBUG ]; then
echo "CMD_TIME: $CMD_TIME"
echo "NUMBER OF $KEY FOUNDS:  $RESULT"
echo "TIMES: $TIME"
echo "TIME TOTAL: $TIMETOT"
echo "TMP: $TMP"
ls $TMP
fi

rm -f $TMP

SURL=`echo $URL | cut -d "/" -f3-4`

MSGOK="Site $SURL key $KEY time $TIMETOT |'time'=${TIMETOT}s;${CRIT}"
MSGKO="Site $SURL has problems, time $TIMETOT |'time'=${TIMETOT}s;${CRIT}"

#PERFDATA HOWTO 'label'=value[UOM];[warn];[crit];[min];[max]

if [ "$RESULT" -ge "1" ] && [ $(echo "$TIMETOT < $CRIT"|bc) -eq 1 ]; then
   echo "OK - $MSGOK"
   exit 0
else
   echo "CRITICAL - $MSGKO"
   exit 2
fi
