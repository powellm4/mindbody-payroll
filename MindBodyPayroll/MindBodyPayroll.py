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
#       
#
#
#
#
#
#

import numpy as np
import pandas as pd
import os

print("\n------------------------------\n\nBeginning MindBody Payroll\n\n------------------------------\n\n\n")

# detect the current working directory
#workingDirectory = os.getcwd()

# create folder for instructor exports
outputFolder = "All_Instructors_CSVs/"
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)


filepath = "MindBodyPayroll/VMAC-01Payroll-RawData-4.csv"
df = pd.read_csv(filepath)
#print(df.head())

#def get_instructors()
for i in range(800):
    intructorsCell = df.loc[i,"Instructors"]
    print(intructorsCell.replace("&", "").strip().split(', '))
    intructorsCell.split

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
