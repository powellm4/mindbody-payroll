# TODO
#  (done)create folder 'All_Instructor_CSVs'
#  (done)check folder for filename
#  (done)open a file stream and write records to it
#  (done)append to existing file
#  (done)drop columns: instructors, revenue, earnings per client, earnings
#  (done)function - compute split rate based on number of instructors
#       (done)identify number of instructors
#       (done)keep track of names of instructors for writing to csv
#       (done)add column pay rate
#       (done)apply multiplier to Rev per session column based on # of instructors
#   (done)get instructor names using the 'instructor' column
#   (done)read in for each instructor file in dat folder    
#   (done)differentiate between 1 and 2 instructors
#   create two separate dataframes, one for each instructor in list
#   write to output file
#
#
#

import numpy as np
import pandas as pd
import glob as glob
import os
from functions import *
print("\n------------------------------\n\nBeginning MindBody Payroll\n\n------------------------------\n\n\n")

#display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

#get list of files from processedData folder
print('Getting processed CSVs from dataProcessing/dat...')
list_of_processed_files = [name for name in os.listdir("dataProcessing/dat") if "02-" in name]

# create folder for instructor exports
outputFolder = "All_Instructors_CSVs/"
create_output_folder(outputFolder)


# for each file in dataProcessing/dat/ folder
for file in list_of_processed_files: 
    df = pd.read_csv("%s%s" % ("dataProcessing/dat/",file))
    instructorsList = get_instructors_list(df)
    df = format_column_headers(df)
    df = drop_unnecessary_columns(df)
    df = assign_instructor_rate(df, len(instructorsList))
    df = assign_amount_due(df)
    write_to_new_csv(df, instructorsList, outputFolder)

print('Done')






