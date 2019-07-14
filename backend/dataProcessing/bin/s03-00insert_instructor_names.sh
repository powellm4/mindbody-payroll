#!/bin/bash
# Insert instructor names for each record
# source ./bin/s03-00insert_instructor_names.sh \
#         ./tmp/s02-01flagSignificantLines.txt
#         #Input-: ./tmp/s02-01flagSignificantLines.txt
#         #Output: ./tmp/s03-01insertedNames.txt

# Create a vim script which inserts the instructor names:
/usr/bin/ex $1 <<EOS
so ./bin/s03-01replaceNames.so
w! ./tmp/s03-02replaceNames.so
q!
EOS

# Insert instructor names for each record:
/usr/bin/ex $1 <<EOS
so ./tmp/s03-02replaceNames.so
g/^?<startPrivate>?/s/^/?<totalFor>?\r/
g/^"Instructors",/s/^/?<m>?/
g/^?<stafName>?/+1s/^?<m>?//
g/^?<startPrivate>?/+1s/^?<m>?//
g/^?<m>?/s//?<totalFor>?\r/
w! ./tmp/s03-01insertedNames.txt
q!
EOS

