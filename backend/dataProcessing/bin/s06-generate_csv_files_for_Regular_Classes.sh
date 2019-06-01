#!/bin/bash
# scriptNAME: s06-generate_csv_files_for_Regular_Classes.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s06-generate_csv_files_for_Regular_Classes.sh $1" #4debug
#source ./bin/s06-generate_csv_files_for_Regular_Classes.sh \
#       ./tmp/07ClassAll.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s06-generate_csv_files_for_Regular_Classes.sh
#----------------------------------------------------------------------
# PURPOSE: Generates one csv file for each set of instructors
#          for Regula Classes
#
# INPUT-: $1
# OUTPUT: ./dat/01-Class-001-<name>.csv
#         ./dat/01-Class-002-<name>.csv
#         ...
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
# Create a vim script for Regular Classes,
# which generate csv files,
# one for each set of instructors:
#-
cat <<'EOF' #4debug
# Create a vim script for Regular Classes,
# which generate csv files,
# one for each set of instructors:
EOF
#-
cat <<'EOF' #4debug
ex $1 <<EOS
so ./bin/12part1.so
w! ./tmp/09ClassPart.1
e! $1
so ./bin/13part2.so
g/^./s/^/01-Class-/
g/^./s/^/.\/dat\//
w! ./tmp/10ClassPart.2
q!
EOS
EOF
#-
ex $1 <<EOS
so ./bin/12part1.so
w! ./tmp/09ClassPart.1
e! $1
so ./bin/13part2.so
g/^./s/^/01-Class-/
g/^./s/^/.\/dat\//
w! ./tmp/10ClassPart.2
q!
EOS

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<'EOF' #4debug
paste ./tmp/09ClassPart.1 ./tmp/10ClassPart.2 \
> ./tmp/11ClassEach.so"
EOF
#-
paste ./tmp/09ClassPart.1 ./tmp/10ClassPart.2 \
> ./tmp/11ClassEach.so

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
# Generate one csv file for each set of instructors
# for Regula Classes:
#-
cat <<'EOF' #4debug
# Generate one csv file for each set of instructors
# for Regula Classes:
EOF
#
cat <<'EOF' #4debug
ex $1 <<EOS
g/?<and>?/s//\&/g
so ./tmp/11ClassEach.so
q!
EOS
EOF
#-
ex $1 <<EOS
g/?<and>?/s//\&/g
so ./tmp/11ClassEach.so
q!
EOS

echo
echo -e "#==================================================\n" #4debug

