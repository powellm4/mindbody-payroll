#!/bin/bash
# Read an input filename (raw) and generate many csv files
# source ./bin/s00-generate_csv_files.sh $fileName

fileName="$1"
#fileName='./raw/Payroll Report 1-1-2019 - 1-31-2019.xls'
#fileName='./raw/Payroll_Report_4-1-2019_4-14-2019.xls'
#fileName='./raw/Payroll Report 5-1-2019 - 5-15-2019.xls'
#fileName='./raw/Payroll Report 6-1-2019 - 6-15-2019.xls'
#fileName='./raw/Payroll_Report_6-1-2019-6-15-2019.xls'

# echo "fileName: \"$fileName\""
# rm -f ./dat/* ./tmp/* ./log/*

cp -a "$fileName" ./tmp/s00-01All.txt

# Convert tabs to spaces and Convert html symbols to text
source ./bin/s01-initial_process.sh \
       ./tmp/s00-01All.txt
       #Input-: ./tmp/s00-01All.txt
       #Output: ./tmp/s01-01All.txt
       #Output: ./tmp/s01-02All.txt

# Do initial cleaning and flag the significat lines
source ./bin/s02-00flag_the_significant_lines.sh \
       ./tmp/s01-02All.txt
       #Input-: ./tmp/s01-02All.txt
       #Output: ./tmp/s02-01flagSignificantLines.txt

# Insert instructor names for each record
source ./bin/s03-00insert_instructor_names.sh \
       ./tmp/s02-01flagSignificantLines.txt
       #Input-: ./tmp/s02-01flagSignificantLines.txt
       #Output: ./tmp/s03-01insertedNames.txt

# Create a csv file for Regular Classes
source ./bin/s04-00Create_csv_file_for_Regular_Classes.sh \
       ./tmp/s03-01insertedNames.txt
       #Input-: ./tmp/s03-01insertedNames.txt
       #Output: ./dat/00-01-Class-All.csv

# Create a csv file for Private Lessons
source ./bin/s05-00Create_csv_file_for_Private_Lessons.sh \
       ./tmp/s03-01insertedNames.txt
       #Input-: ./tmp/s03-01insertedNames.txt
       #Output: ./dat/00-02-Private-All.csv

# Generate one csv file for each set of instructors for Regula Classes
source ./bin/s06-00generate_csv_files_for_Regular_Classes.sh \
       ./tmp/s04-01ClassAll.txt
       #Input-: ./tmp/s04-01ClassAll.txt
       #Output: ./dat/01-Class-001-<instructorName>.txt
       #Output: ./dat/01-Class-002-<instructorName>.txt
       #Output: ./dat/01-Class-...-<instructorName>.txt

# generate one csv file for each set of instructors for Private Lessons:
source ./bin/s07-00generate_csv_files_for_Private_Lessons.sh \
       ./tmp/s05-01PrivateAll.txt
       #Input-: ./tmp/s05-01PrivateAll.txt
       #Output: ./dat/02-Private-001-<instructorName>.txt
       #Output: ./dat/02-Private-002-<instructorName>.txt
       #Output: ./dat/02-Private-...-<instructorName>.txt

