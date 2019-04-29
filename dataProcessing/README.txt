## Follow the following instructions...
## Copy and paste the commands after $> prompt
## \ at the end of line indicate contuation of a command
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
$> cd /home/tseggaikn_gmail_com/dataProcessing
$> rm -f ./dat/* ./tmp/*
$> ./bin/s01-read_a_xls_file_and_generate_many_csv_files.sh \
             Payroll_Report_4-1-2019_4-14-2019.xls \
             &> ./log/Payroll_Report_4-1-2019_4-14-2019.xls.log
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## then review the csv files under dat dir.

https://console.cloud.google.com/compute/instancesDetail/zones/us-west1-a/instances/instance-1?project=vmac-1
