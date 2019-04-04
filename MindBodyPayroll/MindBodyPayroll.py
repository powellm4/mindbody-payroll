# TODO
#  (done)create folder 'All_Instructor_CSVs'
#  (done)check folder for filename
#  (done)open a file stream and write records to it
#  (done)append to existing file
#  drop columns: instructors, revenue, earnings per client, earnings
#  function - compute split rate based on number of instructors
#       (done)identify number of instructors
#       (done)keep track of names of instructors for writing to csv
#       add column pay rate
#       apply multiplier to Rev per session column based on # of instructors
#   get instructor names using the 'instructor' column
#   read in for each instructor file in dat folder    
#
#
#
#
#
#

import numpy as np
import pandas as pd
import glob as glob
import os

print("\n------------------------------\n\nBeginning MindBody Payroll\n\n------------------------------\n\n\n")

#get list of files from processedData folder
list_of_processed_files = [name for name in os.listdir("dataProcessing/dat") if "02-" in name]

# create folder for instructor exports
outputFolder = "All_Instructors_CSVs/"
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

# read in each file in dataProcessing/dat/ folder
for file in list_of_processed_files:
    df = pd.read_csv("%s%s" % ("dataProcessing/dat/",file))

df =  pd.read_csv("MindBodyPayroll/VMAC-01Payroll-RawData-4.csv")
for i in range(800):
    intructorsCell = df.loc[i,"Instructors"]
    print(intructorsCell.replace("&", "").strip().split(', '))
    

#if "&" in intructorsCell:

#name = "Deblin"

# get list of instructor names
# instructors = []
# instructors.append(df.iat[0,0])
# if pd.notna(df.iat[0,1]):
#     instructors.append(df.iat[0,1])
# if pd.notna(df.iat[0,2]):
#     instructors.append(df.iat[0,2])

#print(len(instructors))



# configure file appending
# if os.path.isfile("%s%s.csv" % (outputFolder,name)):
#     mode = "a"
#     print("file exists!")
# else:
#     mode = "w"
#     print("---file does not exist---")
# df.to_csv("%s%s.csv" % (outputFolder,name), mode=mode)
