from functions import *
from flask import *



#
#############################################################
#                                                           #
#        This file should NOT BE USED ANYMORE               #
#                                                           #
#############################################################
#


print("\n------------------------------\n\n"
      "\t   MindBody Payroll\n"
      "\n------------------------------\n\n")


# remove any output data from previous runs
clean_up_dataProcessing_folder()

clean_up_workspace()

create_all_folders()



# test_list = [list_of_public_classes[8]]#, list_of_processed_files[9], list_of_processed_files[10]]

# run dataProcessing shell scripts
file_name = './raw/3-1-3-15.xls'
print("Got here all GOOD")
run_data_processing_shell_scripts(file_name)

# get list of files from dat folder
list_of_public_classes = get_list_of_classes(public=True)
list_of_private_classes = get_list_of_classes(private=True)

# dataFrame for pricing options lookup
po_df = get_pricing_option_lookup_df()

# dataFrame for class name lookup
cn_df = get_class_name_lookup_df()


print("\nWriting public classes to  CSV\n----------")
handle_classes(list_of_public_classes, po_df)


print("\nWriting private classes to  CSV\n----------")
handle_classes(list_of_private_classes, po_df)


print("\n\nWriting instructor dances to CSV\n----------")
export_instructor_dances(po_df)


print("\n\nAppending instructor dances to instructor CSVs\n----------")
append_instructor_dances()


print("\n\nWriting pay stubs with totals\n----------")
output_instructor_totals(cn_df)
