#!/bin/sh 

# Dumps the content of the db file using sqlite commands. dumpdata
# command of manage.py is not working due to inconsistency in the 
# translation.TransactionAction model. This will be useful until 
# the latter is fixed. 
#
# sh dump-bhagirathdb-as-csv.sh
# scp *.zip <target location>
# rm *zip 

DBFILE=$HOME/workspace/bhagirath/shared/bhagirath.db
d=`date +"bhagirathdb-dump-%Y%m%d%H%M%S"`
mkdir -p $d 
cd $d 
for i in `sqlite3 $DBFILE '.tables'  | grep translation` 
do  
/bin/echo -e ".mode csv\n.header on\n.out $i.csv\nselect * from $i;" | sqlite3 $DBFILE
done
cd ..
zip $d.zip $d/*
rm -rf $d 
