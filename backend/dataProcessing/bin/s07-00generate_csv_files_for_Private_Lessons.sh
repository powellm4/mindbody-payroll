#!/bin/bash
# generate one csv file for each set of instructors for Private Lessons:
# source ./bin/s07-00generate_csv_files_for_Private_Lessons.sh \
#        ./tmp/s05-01PrivateAll.txt
#        #Input-: ./tmp/s05-01PrivateAll.txt
#        #Output: ./dat/02-Private-001-<instructorName>.txt
#        #Output: ./dat/02-Private-002-<instructorName>.txt
#        #Output: ./dat/02-Private-...-<instructorName>.txt

# Create a vim script for Private Lessons,
# which generate csv files,
# one for each set of instructors:
/usr/bin/ex $1 <<EOS
so ./bin/s07-01part1Private.so
w! ./tmp/s07-01PrivatePart.1
e! $1
so ./bin/s07-02part2Private.so
g/^./s/^/01-Private-/
g/^./s/^/.\/dat\//
w! ./tmp/s07-02PrivatePart.2
q!
EOS

/usr/bin/paste ./tmp/s07-01PrivatePart.1 ./tmp/s07-02PrivatePart.2 \
> ./tmp/s07-03PrivateEach.so

# Generate one csv file for each set of instructors
# for Regula Privatees:
/usr/bin/ex $1 <<EOS
so ./tmp/s07-03PrivateEach.so
so ./bin/s07-03cleaningPrivate.so
q!
EOS

