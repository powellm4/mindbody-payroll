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
$> ./bin/s00-generate_csv_files.sh './raw/Payroll Report 1-1-2019 - 1-31-2019.xls'
$> ./bin/s00-generate_csv_files.sh './raw/Payroll_Report_4-1-2019_4-14-2019.xls'
$> ./bin/s00-generate_csv_files.sh './raw/Payroll Report 5-1-2019 - 5-15-2019.xls'
$> ./bin/s00-generate_csv_files.sh './raw/Payroll Report 6-1-2019 - 6-15-2019.xls'
$> ./bin/s00-generate_csv_files.sh './raw/Payroll_Report_6-1-2019-6-15-2019.xls'

