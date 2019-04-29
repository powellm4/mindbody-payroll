import pandas as pd
from functions import *
from constants import *

print("\n------------------------------\n\n"
      "MindBody Payroll\n"
      "\n------------------------------\n\n")

# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)


# get list of files from processedData folder
list_of_processed_files = [name for name in os.listdir(input_folder) if "01-Class" in name]

# create folder for instructor exports
create_folder(public_classes_folder)
create_folder(instructor_dance_folder)
create_folder(totals_folder)


# dataFrame for pricing options lookup
po_df = pd.read_csv(special_rates_path)
po_df = format_column_headers(po_df)
po_df = po_df.set_index('Pricing_Option')

# shortlist = [list_of_processed_files[8]]#, list_of_processed_files[9], list_of_processed_files[10]]

# for each file in dataProcessing/dat/ folder
print("\nWriting individual instructor CSVs\n----------")
for file in list_of_processed_files:
    df = pd.read_csv("%s%s" % (input_folder, file))
    instructors_list = get_instructors_list(df)
    df = clean_up_dataframe(df, po_df)
    df = assign_instructor_rate(df, len(instructors_list))
    df = assign_amount_due(df)
    for instructor in instructors_list:
        write_instructor_to_csv(df, instructor)

print("\nExporting instructor dance deduction CSVs\n----------")
export_instructor_dances(po_df)

print("\nAppending instructor dance deduction CSVs\n----------")
append_instructor_dances()

output_instructor_totals()

