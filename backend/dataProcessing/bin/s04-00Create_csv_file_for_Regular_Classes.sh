#!/bin/bash
# Create a csv file for Regular Classes
# source ./bin/s04-00Create_csv_file_for_Regular_Classes.sh \
#        ./tmp/s03-01insertedNames.txt
#        #Input-: ./tmp/s03-01insertedNames.txt
#        #Output: ./dat/00-01-Class-All.csv

ex $1 <<EOS
so ./bin/s04-01prepareClass.so
w! ./tmp/s04-01ClassAll.txt
so ./bin/s04-02cleaning.so
w! ./dat/00-01-Class-All.csv
q!
EOS

