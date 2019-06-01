#!/bin/bash
# scriptNAME: s07-generate_csv_files_for_Private_Lessons.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s07-generate_csv_files_for_Private_Lessons.sh $1" #4debug
#source ./bin/s07-generate_csv_files_for_Private_Lessons.sh \
#       ./tmp/08PrivateAll.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: ./bin/s07-generate_csv_files_for_Private_Lessons.sh
#-
# PURPOSE: Generates one csv file for each set of instructors
#          for Private Lessons
#-
# INPUT-: $1
# OUTPUT: ./dat/02-Private-001-<name>.csv
#         ./dat/02-Private-002-<name>.csv
#         ...
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
# Create a vim script for Private Lessons,
# which generate csv files,
# one for each set of instructors:
#-
cat <<'EOF'
# Create a vim script for Private Lessons,
# which generate csv files,
# one for each set of instructors:
EOF
#-
cat <<'EOF'
ex $1 <<EOS
so ./bin/12part1.so
w! ./tmp/12PrivatePart.1
e! $1
so ./bin/13part2.so
g/^./s/^/02-Private-/
g/^./s/^/.\/dat\//
w! ./tmp/13PrivatePart.2
q!
EOS
EOF
#-
ex $1 <<EOS
so ./bin/12part1.so
w! ./tmp/12PrivatePart.1
e! $1
so ./bin/13part2.so
g/^./s/^/02-Private-/
g/^./s/^/.\/dat\//
w! ./tmp/13PrivatePart.2
q!
EOS

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<'EOF' #4debug
paste ./tmp/12PrivatePart.1 ./tmp/13PrivatePart.2 \
> ./tmp/14PrivateEach.so"
EOF
#-
paste ./tmp/12PrivatePart.1 ./tmp/13PrivatePart.2 \
> ./tmp/14PrivateEach.so

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
# Generate one csv file for each set of instructors
# for Private Lessons:
#-
cat <<'EOF'
# Generate one csv file for each set of instructors
# for Private Lessons:
EOF
#-
cat <<'EOF'
ex $1 <<EOS
g/?<and>?/s//\&/g
so ./tmp/14PrivateEach.so
q!
EOS
EOF
#-
ex $1 <<EOS
g/?<and>?/s//\&/g
so ./tmp/14PrivateEach.so
q!
EOS

echo
echo -e "#==================================================\n" #4debug

