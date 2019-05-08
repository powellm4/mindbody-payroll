#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Follow the following instructions...
   ...Copy and paste the commands after $> prompt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
https://console.cloud.google.com/compute/instancesDetail/zones/us-west1-a/instances/instance-1?project=vmac-1
#-
$> cd /home/tseggaikn_gmail_com/dataProcessing
#-
$> rm -f ./dat/* ./tmp/* ./log/*
#-
$> ./bin/s00-generate_csv_files.sh
#-OR--
$> ./bin/s00-generate_csv_files.sh ./raw/00All.xls
#-OR--
$> fileName=./raw/00All.xls
$> fileName=./raw/Payroll_Report_4-1-2019_4-14-2019.xls
$> ./bin/s00-generate_csv_files.sh $fileName

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## REVIEW: the csv files under dat directory (folder)
$> gview ./dat/00-01-Class-All.csv
$> gview ./dat/00-02-Private-All.csv
$> gview ./dat/...
#-
## REVIEW: the log files under log directory (folder)
$> gview ./log/$(basename $fileName).log

