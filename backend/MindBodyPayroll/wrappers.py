from functions import *

#
#############################################################
#                                                           #
#                          MAIN                             #
#                                                           #
#############################################################
#

def run_backend(filename):
    # calling scripts
    print("\n------------------------------\n\n"
            "\t   MindBody Payroll\n"
            "\n------------------------------\n\n")

    # remove any output data from previous runs
    clean_up_dataProcessing_folder()
    clean_up_workspace()
    create_all_folders()

    # copy file from upload folder to raw folder
    move_uploaded_file(filename)

    # run dataProcessing shell scripts
    # consider adding logic to clear out raw folder
    dir_plus_filename = './raw/' + filename
    run_data_processing_shell_scripts(dir_plus_filename)

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


    print("\n\nCreating unpaid class list\n----------")
    find_unpaid_classes(po_df)
