#!/bin/bash

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate one csv file for each set of instructors for Regula Classes
# source ./bin/s06-00generate_csv_files_for_Regular_Classes.sh \
#        ./tmp/s04-01ClassAll.txt
#        #Input-: ./tmp/s04-01ClassAll.txt
#        #Output: ./dat/01-Class-001-<instructorName>.txt
#        #Output: ./dat/01-Class-002-<instructorName>.txt
#        #Output: ./dat/01-Class-...-<instructorName>.txt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a vim script for Regular Classes,
# which generate csv files,
# one for each set of instructors:
ex $1 <<EOS
so ./bin/s06-01part1Class.so
w! ./tmp/s06-01ClassPart.1
e! $1
so ./bin/s06-02part2Class.so
g/^./s/^/01-Class-/
g/^./s/^/.\/dat\//
w! ./tmp/s06-02ClassPart.2
q!
EOS

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
paste ./tmp/s06-01ClassPart.1 ./tmp/s06-02ClassPart.2 \
> ./tmp/s06-03ClassEach.so

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate one csv file for each set of instructors
# for Regula Classes:
ex $1 <<EOS
so ./tmp/s06-03ClassEach.so
so ./bin/s06-03cleaningClass.so
q!
EOS

