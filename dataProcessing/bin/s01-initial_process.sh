#!/bin/bash
# scriptNAME: s01-initial_process.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s01-initial_process.sh $1" #4debug
#source ./bin/s01-initial_process.sh ./tmp/01All.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s01-initial_process.sh
#-
# PURPOSE: Convert tabs to spaces and Convert html symbols to text
#-
# INPUT-: $1
# I/O---: ./tmp/02All.txt
# OUTPUT: ./tmp/03All.txt
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# 1) Convert tabs to spaces:" #4debug
# 1) Convert tabs to spaces:
#-
echo "expand $1 > ./tmp/02All.txt" #4debug
expand $1 > ./tmp/02All.txt

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "# 2) Convert html symbols to text:" #4debug
# 2) Convert html symbols to text:
#-
cat <<'EOF' #4debug
cat  ./tmp/02All.txt | sed 's/\xC3\xB1/n/g' \
                     | sed 's/\&#241;/n/g'  \
                     | sed 's/\&nbsp;/ /g'  \
                     | sed "s/\&#8217;/'/g" \
                     | sed "s/\&amp;/\&/g"  \
                     | sed "s/\&ndash/-/g"  \
> ./tmp/03All.txt
EOF
#-
cat  ./tmp/02All.txt | sed 's/\xC3\xB1/n/g' \
                     | sed 's/\&#241;/n/g'  \
                     | sed 's/\&nbsp;/ /g'  \
                     | sed "s/\&#8217;/'/g" \
                     | sed "s/\&amp;/\&/g"  \
                     | sed "s/\&ndash/-/g"  \
> ./tmp/03All.txt

echo
echo -e "#==================================================\n" #4debug

