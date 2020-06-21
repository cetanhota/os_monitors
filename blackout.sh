#!/bin/bash

inputgiven="$1"
status=`mysql -h  -p -u  -B -s -e "select active from buster.blackout where host_name=''"`

blackout()
{
#local inputgiven="$1"
if [[ $inputgiven == "blackout" ]] ; then
  echo "Server is already blacked out. Script will now Exit."
  exit 0
else
  echo ""
fi
}

blackout;

mysql -h  -p -u -B -s -e "update buster.blackout set active='yes' where host_name=''"
echo "Server being removed from blackout: Status set to: $inputgiven"
