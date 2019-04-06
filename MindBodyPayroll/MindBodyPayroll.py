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






