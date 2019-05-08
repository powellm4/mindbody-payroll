#!/bin/bash
# scriptNAME: s03-insert_instructor_names.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/ s03-insert_instructor_names.sh $1" #4debug
#source ./bin/s03-insert_instructor_names.sh \
#       ./tmp/04flagSignificantLines.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s03-insert_instructor_names.sh
#-
# PURPOSE: Inserts instructor names for each record
#-
# INPUT-: $1
# I/O---: ./tmp/05replaceNames.so
# OUTPUT: ./tmp/06insertedNames.txt
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# Create a vim script which inserts instructor names:" #4debug
# Create a vim script which inserts the instructor names:
#-
cat <<'EOF' #4debug
ex $1 <<EOS
so ./bin/07replaceNames.so
w! ./tmp/05replaceNames.so
q!
EOS
EOF
#-
ex $1 <<EOS
so ./bin/07replaceNames.so
w! ./tmp/05replaceNames.so
q!
EOS

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# Insert instructor names for each record:" #4debug
# Insert instructor names for each record:
#-
cat <<'EOF' #4debug
ex ./tmp//04flagSignificantLines.txt <<EOS
so ./tmp/05replaceNames.so
w! ./tmp/06insertedNames.txt
q!
EOS
EOF
#-
ex ./tmp//04flagSignificantLines.txt <<EOS
so ./tmp/05replaceNames.so
w! ./tmp/06insertedNames.txt
q!
EOS

echo
echo -e "#==================================================\n" #4debug

