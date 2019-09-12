from data_cleaner import run_data_cleaner
from functions import *
from db_helper import *
import config


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
    # clean_up_dataProcessing_folder()#dp
    clean_up_workspace()
    create_all_folders()
    with create_connection(database_path) as conn:
        wipe_database(conn)
        create_table(conn, config.sql_create_instructors_table)

    # copy file from upload folder to raw folder
    move_uploaded_file(filename)

    # run dataProcessing shell scripts
    # consider adding logic to clear out raw folder
    # dir_plus_filename = './raw/' + filename#dp
    # run_data_processing_shell_scripts(dir_plus_filename)#dp
    run_data_cleaner(filename)


    # get list of files from dat folder
    # list_of_public_classes = get_list_of_classes(public=True)#dp
    # list_of_private_classes = get_list_of_classes(private=True)#dp
    # remove_bad(list_of_public_classes)#dp
    # remove_bad(list_of_private_classes)#dp
    # list_of_public_classes = get_list_of_classes(public=True)#dp
    # list_of_private_classes = get_list_of_classes(private=True)#dp

    #dc
    list_of_dc_classes = get_dc_list_of_classes()


    # dataFrame for pricing options lookup
    po_df = get_pricing_option_lookup_df()

    # dataFrame for class name lookup
    cn_df = get_class_name_lookup_df()

    pay_period = get_pay_period_from_filename(filename)
    set_global_pay_period(pay_period)




    # print("\nWriting public classes to  CSV\n----------") #dp
    # handle_classes(list_of_public_classes, po_df)#dp
    print("\nHandling DataCleaner output\n----------")
    handle_dc_classes(list_of_dc_classes, po_df)



    # print("\nWriting private classes to  CSV\n----------")#dp
    # handle_classes(list_of_private_classes, po_df)#dp




    # print("\n\nWriting instructor dances to CSV\n----------")#dp
    # export_instructor_dances(po_df)#dp
    print("\n\ndata cleaner instructor dances..\n----------")
    handle_dc_instructor_dances(po_df)



    # print("\n\nAppending instructor dances to instructor CSVs\n----------")#dp
    # append_instructor_dances()#dp
    dc_append_instructor_dances()


    print("\n\nWriting pay stubs with totals\n----------")#dp
    # output_instructor_totals(cn_df)#dp
    dc_output_instructor_totals(cn_df)


    # print("\n\nCreating unpaid class list\n----------")#dp
    # find_unpaid_classes(po_df, all_classes_path)#dp
    # find_unpaid_classes(po_df, all_private_classes_path)#dp
    dc_find_unpaid_classes(po_df, all_classes_path)
