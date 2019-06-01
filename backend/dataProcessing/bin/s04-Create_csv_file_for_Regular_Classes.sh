#!/bin/bash
# scriptNAME: s04-Create_csv_file_for_Regular_Classes.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s04-Create_csv_file_for_Regular_Classes.sh $1" #4debug
#source ./bin/s04-Create_csv_file_for_Regular_Classes.sh \
#       ./tmp/06insertedNames.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME ./bin/s04-Create_csv_file_for_Regular_Classes.sh
#-
# PURPOSE: Creates a csv file for regular Classes
#
# INPUT-: $1
# I/O---: ./tmp/07ClassAll.txt
# OUTPUT: ./dat/00-01-Class-All.csv
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# Create a csv file for regular Classes:" #4debug
# Create a csv file for regular Classes:
#-
cat <<'EOF' #4debug
ex $1 <<EOS
so ./bin/08prepareClass.so
w! ./tmp/07ClassAll.txt
so ./bin/09cleaning.so
w! ./dat/00-01-Class-All.csv
q!
EOS
EOF
#-
ex $1 <<EOS
so ./bin/08prepareClass.so
w! ./tmp/07ClassAll.txt
so ./bin/09cleaning.so
w! ./dat/00-01-Class-All.csv
q!
EOS

echo
echo -e "#==================================================\n" #4debug

