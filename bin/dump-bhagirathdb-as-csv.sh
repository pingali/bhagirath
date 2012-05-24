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
