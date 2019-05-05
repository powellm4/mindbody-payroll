import pandas as pd
from functions import *
from constants import *
import shutil

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
list_of_public_classes = [name for name in os.listdir(dat_folder_path) if "01-Class" in name]
list_of_privates = [name for name in os.listdir(dat_folder_path) if "02-Private" in name]


# remove any output data from previous runs
clean_up_workspace()


# create folders for outputs
create_folder(public_classes_folder_path)
create_folder(private_classes_folder_path)
create_folder(instructor_dance_folder_path)
create_folder(totals_folder_path)


# dataFrame for pricing options lookup
po_df = pd.read_csv(pricing_options_path)
po_df = format_column_headers(po_df)
po_df = po_df.set_index('Pricing_Option')


# cn_df = pd.read_csv(class_name_lookup_path)
# cn_df = format_column_headers(cn_df)
# cn_df = po_df.set_index('Pricing_Option')
# print(cn_df.head())

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
