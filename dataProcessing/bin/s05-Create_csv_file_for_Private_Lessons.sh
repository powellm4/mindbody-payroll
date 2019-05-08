#!/bin/bash
# scriptNAME: s05-Create_csv_file_for_Private_Lessons.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s05-Create_csv_file_for_Private_Lessons.sh $1" #4debug
#source ./bin/s05-Create_csv_file_for_Private_Lessons.sh \
#       ./tmp/06insertedNames.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s05-Create_csv_file_for_Private_Lessons.sh
#-
# Create a csv file for Private Lessons
#
# Input-: $1
# I/O---: ./tmp/08PrivateAll.txt
# Output: ./dat/00-02-Private-All.csv
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# Create a csv file for Private Lessons:" #4debug
# Create a csv file for Private Lessons:
#-
cat <<'EOF' #4debug
ex $1 <<EOS
so ./bin/10preparePrivate.so
w! ./tmp/08PrivateAll.txt
so ./bin/11cleaning.so
w! ./dat/00-02-Private-All.csv
q!
EOS
EOF
#-
ex $1 <<EOS
so ./bin/10preparePrivate.so
w! ./tmp/08PrivateAll.txt
so ./bin/11cleaning.so
w! ./dat/00-02-Private-All.csv
q!
EOS

echo
echo -e "#==================================================\n" #4debug

