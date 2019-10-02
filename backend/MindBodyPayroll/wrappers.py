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
    print("\n------------------------------\n\n"
            "\t   MindBody Payroll\n"
            "\n------------------------------\n\n")


    # remove any output data from previous runs
    clean_up_workspace()
    create_all_folders()
    with create_connection(database_path) as conn:
        wipe_instructors_database(conn)
        create_table(conn, config.sql_create_instructors_table)
        create_table(conn, config.sql_create_auth_code_table)

    run_data_cleaner(filename)

    list_of_dc_classes = get_dc_list_of_classes()

    # dataFrame for pricing options lookup
    po_df = get_pricing_option_lookup_df()

    # dataFrame for class name lookup
    cn_df = get_class_name_lookup_df()

    pay_period = get_pay_period_from_filename(filename)
    set_global_pay_period(pay_period)

    print("\nHandling DataCleaner Output\n----------")
    handle_dc_classes(list_of_dc_classes, po_df)

    print("\n\nHandling Instructor Dances\n----------")
    handle_dc_instructor_dances(po_df)

    dc_append_instructor_dances()


    print("\n\nWriting pay stubs with totals\n----------")
    dc_output_instructor_totals(cn_df)


    dc_find_unpaid_classes(po_df, all_classes_path)
    print("\n\nCreated unpaid class list\n")
