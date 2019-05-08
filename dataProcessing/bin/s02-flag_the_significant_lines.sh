#!/bin/bash
# scriptNAME: s02-flag_the_significant_lines.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s02-flag_the_significant_lines.sh $1" #4debug
#source ./bin/s02-flag_the_significant_lines.sh ./tmp/03All.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s02-flag_the_significant_lines.sh
#-
# PURPOSE: Does initial cleaning and markups (flags) significat lines
#-
# INPUT-: $1 
# OUTPUT: ./tmp/02flagSignificantLines.txt
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# Do initial cleaning and markup (flag) significat lines:" #4debug
# Do initial cleaning and markup (flag) significat lines:
#-
cat <<'EOF' #4debug
ex $1 <<EOS
so ./bin/01cleaning.so
so ./bin/02markBasics.so
so ./bin/03markData.so
so ./bin/04cleaning.so
so ./bin/05joinData.so
so ./bin/06addColumns.so
w! ./tmp//04flagSignificantLines.txt
q!
EOS
EOF
#-
ex  $1 <<EOS
so ./bin/01cleaning.so
so ./bin/02markBasics.so
so ./bin/03markData.so
so ./bin/04cleaning.so
so ./bin/05joinData.so
so ./bin/06addColumns.so
w! ./tmp//04flagSignificantLines.txt
q!
EOS

echo
echo -e "#==================================================\n" #4debug

