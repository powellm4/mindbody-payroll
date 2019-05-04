import pandas as pd
from functions import *
from constants import *

print("\n------------------------------\n\n"
      "\t   MindBody Payroll\n"
      "\n------------------------------\n\n")

# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)


# get list of files from processedData folder
list_of_public_classes = [name for name in os.listdir(dat_folder) if "01-Class" in name]
list_of_privates = [name for name in os.listdir(dat_folder) if "02-Private" in name]

# create folders for outputs
create_folder(public_classes_folder)
create_folder(private_classes_folder)
create_folder(instructor_dance_folder)
create_folder(totals_folder)


# dataFrame for pricing options lookup
po_df = pd.read_csv(pricing_options_path)
po_df = format_column_headers(po_df)
po_df = po_df.set_index('Pricing_Option')

# test_list = [list_of_processed_files[8]]#, list_of_processed_files[9], list_of_processed_files[10]]




#
#############################################################
#                                                           #
#                          MAIN                             #
#                                                           #
#############################################################
#

print("\nWriting public classes to  CSV\n----------")
handle_classes(list_of_public_classes, po_df)

print("\nWriting private classes to  CSV\n----------")
handle_classes(list_of_privates, po_df)

print("\n\nWriting instructor dances to CSV\n----------")
export_instructor_dances(po_df)

print("\n\nAppending instructor dances to instructor CSVs\n----------")
append_instructor_dances()

print("\n\nWriting pay stubs with totals\n----------")
output_instructor_totals()

