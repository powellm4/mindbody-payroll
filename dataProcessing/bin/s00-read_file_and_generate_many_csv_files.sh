#!/bin/bash
# scriptNAME: s00-read_file_and_generate_many_csv_files.sh

echo -e "\n#--------------------------------------------------" #4debug
echo "Date: $(date)" #4debug
echo "source ./bin/s00-read_file_and_generate_many_csv_files.sh $1" #4debug
#source ./bin/s00-read_file_and_generate_many_csv_files.sh $fileName \
#|tee ./log/$(basename $fileName).log

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "fileName: \$1 $1" #4debug

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
cat <<EOF #4debug
# scriptNAME: s00-read_file_and_generate_many_csv_files.sh
#-
# PURPOSE: Reads an input filename (raw) and generates many csv files
#-
# INPUT-: $1
# OUTPUT: ./tmp/*.*
# OUTPUT: ./dat/*.*
EOF

echo -e "\n#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #4debug
echo "cp -a $1 ./tmp/01All.txt" #4debug
cp -a $1 ./tmp/01All.txt

echo
echo "source ..." #4debug

echo
echo -e "#==================================================\n" #4debug

#######################################################################
# Convert tabs to spaces and Convert html symbols to text
source ./bin/s01-initial_process.sh ./tmp/01All.txt

# Do initial cleaning and markup (flag) significat lines
source ./bin/s02-flag_the_significant_lines.sh ./tmp/03All.txt

# Insert instructor names for each record
source ./bin/s03-insert_instructor_names.sh \
       ./tmp/04flagSignificantLines.txt

# Create a csv file for Regular Classes
source ./bin/s04-Create_csv_file_for_Regular_Classes.sh \
       ./tmp/06insertedNames.txt

# Create a csv file for Private Lessons
source ./bin/s05-Create_csv_file_for_Private_Lessons.sh \
       ./tmp/06insertedNames.txt

# Generate one csv file for each set of instructors for Regula Classes
source ./bin/s06-generate_csv_files_for_Regular_Classes.sh \
       ./tmp/07ClassAll.txt

# generate one csv file for each set of instructors for Private Lessons:
source ./bin/s07-generate_csv_files_for_Private_Lessons.sh \
       ./tmp/08PrivateAll.txt

