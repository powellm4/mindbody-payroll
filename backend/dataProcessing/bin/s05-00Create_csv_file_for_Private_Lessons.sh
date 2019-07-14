#!/bin/bash
# Create a csv file for Private Lessons
# source ./bin/s05-00Create_csv_file_for_Private_Lessons.sh \
#        ./tmp/s03-01insertedNames.txt
#        #Input-: ./tmp/s03-01insertedNames.txt
#        #Output: ./dat/00-02-Private-All.csv

# Create a csv file for Private Lessons:
/usr/bin/ex $1 <<EOS
so ./bin/s05-01preparePrivate.so
w! ./tmp/s05-01PrivateAll.txt
so ./bin/s05-02cleaning.so
w! ./dat/00-02-Private-All.csv
q!
EOS

