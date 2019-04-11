import pandas as pd
from functions import *

print("\n------------------------------\n\nBeginning MindBody Payroll\n\n------------------------------\n\n\n")

# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)

input_folder = "../dataProcessing/dat/"
output_folder = "../allInstructorsCSVs/"
special_rates_path = "../lookupTables/pricing-options.csv"


# get list of files from processedData folder
print('Getting processed CSVs from dataProcessing/dat...')
list_of_processed_files = [name for name in os.listdir(input_folder) if "02-" in name]

# create folder for instructor exports
create_output_folder(output_folder)


# dataframe for pricing options lookup
po_df = pd.read_csv(special_rates_path)
po_df = format_column_headers(po_df)
po_df = po_df.set_index('Pricing_Option')


# for each file in dataProcessing/dat/ folder
for file in list_of_processed_files:
    df = pd.read_csv("%s%s" % (input_folder, file))
    instructors_list = get_instructors_list(df)
    df = format_column_headers(df)
    df = drop_unnecessary_columns(df)
    df = assign_instructor_rate(df, len(instructors_list))
    df = include_pricing_options(df, po_df)
    df = assign_amount_due(df)
    write_to_new_csv(df, instructors_list, output_folder)

print('Done')
