#!/bin/bash
# scriptNAME: s00-generate_csv_files.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s00-generate_csv_files.sh" #4debug
#./bin/s00-generate_csv_files.sh
#./bin/s00-generate_csv_files.sh ./raw/00All.xls
#./bin/s00-generate_csv_files.sh ./raw/Payroll_Report_4-1-2019_4-14-2019.xls

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
if [ ! -z "$1"  ]; then
  fileName=$1
else
  echo "\$1 is NOT empty"
  read -p "Enter the input fileName [./raw/00All.xls]: " fileName
  fileName=${path:-./raw/00All.xls}
fi
echo "fileName: $fileName" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s00-generate_csv_files.sh
#-
# PURPOSE: Reads an input filename (raw) and generates many csv files
#-
# INPUT-: $fileName
# OUTPUT: ./tmp/*.*
# OUTPUT: ./dat/*.*
# OUTPUT: ./log/$(basename $fileName).log
EOF

echo
echo "source ..." #4debug

echo
echo -e "#==================================================\n" #4debug

#######################################################################
# Read an input filename (raw) and generate many csv files
source ./bin/s00-read_file_and_generate_many_csv_files.sh $fileName \
|tee ./log/$(basename $fileName).log

cat <<EOF #4debug
#######################################################################
Review: ./log/$(basename $fileName).log
#######################################################################
EOF

