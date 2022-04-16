#!/bin/bash
set -e
 
echo '1.Starting mysql....'
#Starting mysql
service mysql start
sleep 3
echo `service mysql status`
 
echo '2.Importing data....'
#import data
mysql < /mysql/comp7940_Group40.sql
 
sleep 3
echo `service mysql status`
 
#Reset mysql passwd
mysql < /mysql/createuser.sql
 
tail -f /dev/null