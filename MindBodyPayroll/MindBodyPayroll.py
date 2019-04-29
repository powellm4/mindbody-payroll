#   To do:
#
#   at end of program, combine two csvs for each instructor
#   add total and append it to csv bottom


import pandas as pd
from functions import *
from constants import *

print("\n------------------------------\n\n"
      "Beginning MindBody Payroll\n"
      "\n------------------------------\n\n")

# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)




# get list of files from processedData folder
print('Getting processed CSVs from dataProcessing/dat...')
list_of_processed_files = [name for name in os.listdir(input_folder) if "01-" in name]

# create folder for instructor exports
create_folder(output_folder)
create_folder(instructor_dance_folder)
create_folder(concatenated_csvs_folder)


# dataFrame for pricing options lookup
po_df = pd.read_csv(special_rates_path)
po_df = format_column_headers(po_df)
po_df = po_df.set_index('Pricing_Option')

shortlist = [list_of_processed_files[0]]#, list_of_processed_files[9], list_of_processed_files[10]]

# for each file in dataProcessing/dat/ folder
for file in list_of_processed_files:
    df = pd.read_csv("%s%s" % (input_folder, file))
    instructors_list = get_instructors_list(df)
    df = clean_up_dataframe(df, po_df)
    df = assign_instructor_rate(df, len(instructors_list))
    df = assign_amount_due(df)
    for instructor in instructors_list:
        write_instructor_to_csv(df, instructor)

export_instructor_dances(po_df)


instructor_csv_list = [name for name in os.listdir(output_folder)]
instructor_dance_list = [name for name in os.listdir(instructor_dance_folder)]
for file in instructor_csv_list:
    if file in instructor_dance_list:
        print('found  ' + file)
        df2 = pd.read_csv('%s%s' % (instructor_dance_folder, file))
        print("appending %s " % file)
        df2.to_csv("%s%s" % (output_folder, file), mode="a", index=False, header=False)

print("\n\n")
for file in instructor_dance_list:
    if file not in instructor_csv_list:
        print('Instructor Dance: %s not found as an Instructor for pay period' % file)

print('Done')
