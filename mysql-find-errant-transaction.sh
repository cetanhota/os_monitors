#!/bin/bash

scriptname=$(basename -- "$0")
errant_first=0
errant_last=0

############################################################
# Help                                                     #
############################################################
help()
{
   # Display Help
   echo "MySQL find and report errant transactions."
   echo
   echo "Options:"
   echo "-p | --primary     <required> Primary Host name."
   echo "-r | --replica     <required> Replica Host name."
   echo "-e | --email       <optional> E-mail."
   echo "-h | --help        Show Help."
   echo "Example:           $scriptname -p primary server -r replica server"
   echo
}
######################################
# Process the input options.         #
######################################
# Get the options
while [ "$1" != "" ]; do
   case $1 in
       # Primary host
         --primary | -p )
         shift
         primary=$1
         ;;
       # Replica host
         --replica | -r )
         shift
         replica=$1
         ;;
       # email address
         --email | -e )
         shift
         email=$1
         ;;
       # display Help
         help | -help | --help )
         help
         exit
         ;;
         * )
         help
         exit
   esac
   shift
done

if [ "$primary" = "" ] || [ "$replica" = "" ]; then
  help
fi

primary_set=$(mysql -h "$primary" -u root -rNB -e " show variables like 'gtid_executed';" | sed 's/\<gtid_executed\>//g')
replica_set=$(mysql -h "$replica" -u root -rNB -e " show variables like 'gtid_executed';" | sed 's/\<gtid_executed\>//g')

# errant transaction(s) find and report
results()
{
  subset=$(mysql -h "$replica" -u root -rNB -e "select gtid_subset('$replica_set','$primary_set') as subset;")

  if [[ "$subset" -eq "1" ]] ; then
    echo "No Errant transaction(s) found."
    exit 0
  else
    errant=$(mysql -h "$replica" -u root -rNB -e "select gtid_subtract('$replica_set','$primary_set') as errant;")
    echo "Errant transaction(s) found: ${errant}"
  fi
}

# repair function
repair()
{
  clear
  echo "Errant transaction(s): ${errant}"
  read -p "Do you want to repair the Errant transactions(s) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]] ; then
    echo "No repairs requested."
    exit 0
  else
    errant_first=$(echo -e "${errant}" | cut -d: -f2- | cut -d- -f1) # first errant
    errant_last=$(echo -e "${errant}" | cut -d: -f2- | cut -d- -f2) # last errant
    echo "$errant_first"
    echo "$errant_last"

    COUNT=$errant_last
    while [ $COUNT -le $errant_last ]; then
      let COUNT=COUNT-1
    done
    fi
}

email() # email function
{
  if [[ "$email" = "" ]] ; then
    exit 0
  else
    echo " send email " | mailx -s 'subject' -f you.com "$email"
 fi
}

results
if [[ "${subset}" -eq "0" ]] ; then
  echo "repairs needed ${errant}"
  repair
fi
email
