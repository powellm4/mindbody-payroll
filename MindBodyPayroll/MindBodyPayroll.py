#   To do:
#   read in raw file?
#       look for VMAC INSTRUCTOR CLASS
#       for each row, write to file
#           solution: write all file names as reira
#           pros: no lookup table required.. i.e. no maintenance by user.
#           cons: possible null reference type errors? if 02- instructors are missing a last name
#           solution:
#   read in 00-01-Class-All.csv
#   filter down to VMAC INSTRUCTOR CLASS entries
#   group by student name
#   write to csv in instructorClasses folder
#
#   at end of program, combine two csvs for each instructor
#   add total and append it to csv bottom


import pandas as pd
from functions import *

print("\n------------------------------\n\n"
      "Beginning MindBody Payroll\n"
      "\n------------------------------\n\n")

# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)

input_folder = "../dataProcessing/dat/"
output_folder = "../allInstructorsCSVs/"
instructor_dance_folder = "../instructorDances/"
special_rates_path = "../lookupTables/pricing-options.csv"


# get list of files from processedData folder
print('Getting processed CSVs from dataProcessing/dat...')
list_of_processed_files = [name for name in os.listdir(input_folder) if "01-" in name]

# create folder for instructor exports
create_output_folder(output_folder)
create_output_folder(instructor_dance_folder)


# dataFrame for pricing options lookup
po_df = pd.read_csv(special_rates_path)
po_df = format_column_headers(po_df)
po_df = po_df.set_index('Pricing_Option')

shortlist = [list_of_processed_files[0]]#, list_of_processed_files[9], list_of_processed_files[10]]

# for each file in dataProcessing/dat/ folder
for file in shortlist:
    df = pd.read_csv("%s%s" % (input_folder, file))
    instructors_list = get_instructors_list(df)
    df = clean_up_dataframe(df, po_df)
    df = assign_instructor_rate(df, len(instructors_list))
    df = assign_amount_due(df)
    #print(df.head())
    write_instructor_to_csv(df, instructors_list, output_folder)

export_instructor_dances(input_folder, po_df)

print('Done')
