#!/bin/bash
# Do initial cleaning and flag the significat lines
# source ./bin/s02-00flag_the_significant_lines.sh \
#        ./tmp/s01-02All.txt 
#        #Input-: ./tmp/s01-02All.txt
#        #Output: ./tmp/s02-01flagSignificantLines.txt

ex  $1 <<EOS
so ./bin/s02-01cleaning.so
so ./bin/s02-02markBasics.so
so ./bin/s02-03markData.so
so ./bin/s02-04cleaning.so
so ./bin/s02-05joinData.so
so ./bin/s02-06addColumns.so
w! ./tmp/s02-01flagSignificantLines.txt
q!
EOS

