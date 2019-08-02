#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## Follow the following instructions...
   ...Copy and paste the commands after $> prompt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
https://console.cloud.google.com/compute/instancesDetail/zones/us-west1-a/instances/instance-1?project=vmac-1
#-
_x $> cd ~/.../dataProcessing
__ $> cd /home/tseggai/00tkn/00prj
__ $> cd ./00.nuatu/dataProcessing
#-
__ $> rm -f ./dat/* ./tmp/* ./log/*
#-
__ $> ./bin/s00-generate_csv_files.sh \
      './raw/Payroll Report 7-16-2019 - 7-31-2019.xls'

