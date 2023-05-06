import os
import re
import shutil
import subprocess
import sys

import pandas as pd
import pdfkit

import config
from constants import *
from db_helper import *
from pdf_helper import create_html_paystub_file, add_table_to_html_paystub_file

# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format

# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)


# the main function for processing a list of classes
# makes calls to helper functions and outputs a csv for each instructor
def handle_dc_classes(list_of_classes, po_df, ipo_df):
    # add in instructor pricing
    po_df = pd.concat([po_df, ipo_df])
    # for each (public/private) class file in dataProcessing/dat/ folder
    for file in list_of_classes:
        df = pd.read_csv("%s%s" % (output_folder_path +
                                   data_cleaner_output_folder, file))
        instructors_list = get_instructors_list(df)
        if po_df is not None:
            df = include_pricing_options(df, po_df)
        df = assign_instructor_rate(df, len(instructors_list))
        df = assign_amount_due(df)
        for instructor in instructors_list:
            # add_instructor_to_db()
            update_instructor_csv(df, instructor, dc_classes_folder_path)


# input: 'Instructors' cell from processed data
# output: Array of instructor(s), formatted as F.Last
def get_instructors_list(df):
    instructors_cell = df.loc[0, "Instructors"]
    if "&" in instructors_cell:
        instructors = instructors_cell.replace("&", "").strip().split(', ')
        for i in range(len(instructors)):
            temp = instructors[i].split()
            last = temp[1]
            first = temp[0][0]
            full = first + "." + last
            instructors[i] = full
    else:
        instructors = [instructors_cell]
        for i in range(len(instructors)):
            temp = instructors[i].split(', ')
            first = temp[1]
            first = first[0]
            last = temp[0].replace(",", "").replace(' ', '-').strip()
            full = first + "." + last
            instructors[i] = full
    return instructors


# adds the instructor rate column to a dataframe
def assign_instructor_rate(df, no_of_instructors=None):
    if no_of_instructors is not None:
        return df.assign(Rate=1.0 / no_of_instructors)
    else:
        return df.assign(Rate=1.0)


def format_column_headers(df):
    df.columns = [c.strip() for c in df.columns]
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df.columns = [c.replace('.', '') for c in df.columns]
    df.columns = [c.replace('"', '') for c in df.columns]
    df.columns = [c.replace('Appointment', 'Class') for c in df.columns]
    df.columns = [c.replace('Appt', 'Class') for c in df.columns]
    return df


# given a name in First Last format,
# return name in F.Last format
def format_name(name):
    if ' ' in name:
        arr = name.split(' ')
        first = arr[0][0]
        last = ''
        for i in range(1, len(arr)):
            if i == 1:
                last = last + arr[i]
            else:
                last = last + '-' + arr[i]
        return first + '.' + last
    else:
        return name


# creates the [folder] inside the /output/ folder
def create_folder(folder):
    if not os.path.exists('../output/'):
        os.mkdir('../output/')
    if not os.path.exists(folder):
        os.mkdir(folder)


# creates the Amount Due To Instructor column
# with correct amount
def assign_amount_due(df):
    df.Instructor_Pay = df.Instructor_Pay.str.replace("$", "")
    df = df.assign(Amount_Due_To_Instructor=(
            df.Instructor_Pay.astype(float) * df.Rate).round(3))
    return df


# decides whether an instructors csv already exists,
# writing to a new csv if not
# appending to existing csv if so
# provide_feedback allows you to turn off print statements
def update_instructor_csv(df, instructor, output_folder, provide_feedback=True, instructor_dance=False):
    if not instructor_dance:
        df['Instructors'] = instructor
    if os.path.isfile("%s%s.csv" % (output_folder, instructor)):
        mode = "a"
        include_header = False
        if provide_feedback:
            print("Found %s CSV, appending new data" % instructor)
    else:
        mode = "w"
        include_header = True
        if provide_feedback:
            print("Writing %s to new CSV..." % instructor)
    df.to_csv("%s%s.csv" % (output_folder, instructor),
              mode=mode, header=include_header, index=False)


# prepares the class name lookup dataframe for
# merging into main df
def clean_up_class_name_dataframe(cn_df):
    cn_df = format_column_headers(cn_df)
    cn_df.Day = cn_df.Day.map(dict(
        Mondays=0, Tuesdays=1, Wednesdays=2, Thursdays=3, Fridays=4, Saturdays=5, Sundays=6))
    cn_df.Name = cn_df.Name.apply(format_name)
    cn_df.Time = cn_df.Time.str.replace("PM", "pm")
    cn_df.Time = cn_df.Time.str.replace("AM", "am")
    return cn_df


# merges the dataFrame with the pricing options dataFrame to allow lookup of pricing options
def include_pricing_options(df, po_df):
    # df['lower'] = df.Series_Used.str.lower()
    # po_df['lower'] = po_df.index.str.lower()
    # return pd.merge(df, po_df, left_on='lower', right_on='lower', how='left')
    po_df['lower'] = po_df.index
    new_df = pd.merge(df, po_df, left_on='Series_Used',
                      right_on='lower', how='left')
    new_df = new_df.drop(columns=['lower'])
    return new_df


# merges the class name lookup dataframe with the main dataframe,
# adds; the class column
def include_class_names(df, cn_df):
    return df
    df.Class_Time = df.Class_Time.str.replace('\xa0', ' ')
    df['Day'] = pd.to_datetime(df.Class_Date).dt.weekday
    merged_df = pd.merge(df, cn_df, left_on=['Day', 'Instructors', 'Class_Time'],
                         right_on=['Day', 'Name', 'Time'], how='left')
    merged_df = merged_df.drop(columns=['Day', 'Name', 'Time'])
    merged_df = merged_df[['Instructors', 'Class', 'Class_Date', 'Class_Time',
                           'Client_Name', 'Series_Used', 'Revenue_per_class',
                           'Instructor_Pay', 'Rate', 'Amount_Due_To_Instructor']]
    return merged_df


# takes the original dataFrame with all classes and writes
#   all instructor dances to their own file
# inputs: dat_folder - contains full data csv
#           pd_df - pricing lookup dataFrame
def handle_dc_instructor_dances(ipo_df):
    file = all_classes_path
    df = pd.read_csv("%s%s" % (output_folder_path +
                               data_cleaner_output_folder, file))

    filter_values = ipo_df.index.values
    df = df[df['Series_Used'].isin(filter_values)]

    df = include_pricing_options(df, ipo_df)
    df = assign_instructor_rate(df)
    df = df.drop_duplicates()
    df = assign_amount_due(df)
    df = filter_out_jamal_carolina_classes(df)
    df.Amount_Due_To_Instructor = df.Amount_Due_To_Instructor * -2
    unique_instructors = df.Client_Name.unique()
    for instructor in unique_instructors:
        udf = df[df.Client_Name == instructor]
        update_instructor_csv(
            udf, instructor, dc_classes_folder_path, instructor_dance=True)


# instructors get free classes if the class is taught by carolina and jamal
# removed all classes taught by carolina and or jamal from dataframe
def filter_out_jamal_carolina_classes(df):
    return df[~df.Instructors.str.contains('Jamal|Carolina', case=False, regex=True)]


# adds deduction rows to the files found in publicClasses folder
def dc_append_instructor_dances():
    instructor_csv_list = [name for name in os.listdir(dc_classes_folder_path)]
    instructor_dance_list = [name for name in os.listdir(
        dc_instructor_dance_folder_path)]
    for file in instructor_csv_list:
        if file in instructor_dance_list:
            iddf = pd.read_csv('%s%s' %
                               (dc_instructor_dance_folder_path, file))
            print("appending %s " % file)
            iddf.to_csv("%s%s" % (dc_classes_folder_path, file),
                        mode="a", index=False, header=False)

    print("\n\nList of Instructor dances with no matching instructor CSV\n----------")
    total_missing = 0
    for file in instructor_dance_list:
        if file not in instructor_csv_list:
            total_missing = total_missing + 1
            print('Instructor Dance: %s not found as an Instructor for pay period' % file)
            # name = file.replace(".csv", "")
            # check_against_family_lookup(name)
    if total_missing == 0:
        print('(empty)')


# writes csv to totals folder containing total for instructor
def dc_output_instructor_totals(cn_df):
    for file in os.listdir(dc_classes_folder_path):
        print('Creating pay stub for %s' % file.replace('.csv', ''))
        df = pd.read_csv("%s%s" % (dc_classes_folder_path, file))
        df = include_class_names(df, cn_df)
        df = df.append(df.sum(numeric_only=True), ignore_index=True)
        # df.iloc[-1][0] = 'Total'

        df.to_csv("%s%s" % (dc_totals_folder_path, file),
                  mode="w", index=False)
        with create_connection(database_path) as conn:
            instructor = (file, 0)
            create_instructor(conn, instructor)


# removes any data generated by previous runs
def clean_up_workspace():
    if os.path.isdir(output_folder_path):
        shutil.rmtree(output_folder_path)


# reads in pricing lookup table &
# prepares it for processing and merging
def get_pricing_option_lookup_df():
    po_df = pd.read_csv(pricing_options_path)
    po_df = format_column_headers(po_df)
    po_df = po_df.set_index('Pricing_Option')
    return po_df


# reads in instructor dance option lookup table &
# prepares it for processing and merging
def get_instructor_pricing_option_lookup_df():
    po_df = pd.read_csv(instructor_prices_options_path)
    po_df = format_column_headers(po_df)
    po_df = po_df.set_index('Pricing_Option')
    return po_df


# reads in class name lookup table &
# prepares it for processing and merging
def get_class_name_lookup_df():
    cn_df = pd.read_csv(class_name_lookup_path)
    cn_df = clean_up_class_name_dataframe(cn_df)
    return cn_df


# creates folders for outputs
def create_all_folders():
    create_folder(public_classes_folder_path)
    create_folder(unpaid_folder_path)
    create_folder(private_classes_folder_path)
    create_folder(instructor_dance_folder_path)
    create_folder(totals_folder_path)
    create_folder(output_folder_path)
    create_folder(export_folder_path)
    create_folder(export_html_folder_path)
    create_folder(export_pdf_folder_path)
    # create dc folders
    create_folder(dc_classes_folder_path)
    create_folder(dc_export_folder_path)
    create_folder(dc_export_html_folder_path)
    create_folder(dc_export_pdf_folder_path)
    create_folder(dc_instructor_dance_folder_path)
    create_folder(dc_unpaid_folder_path)
    create_folder(dc_totals_folder_path)


# gets list of file names from the dc output folder
def get_dc_list_of_classes():
    return [name for name in os.listdir(output_folder_path + data_cleaner_output_folder) if
            not name.startswith('00-01')]


# opens file in totals folder, adds adjustment, recalculates total and rewrites file
# input - description - is added under the Series_Used column
def make_adjustment(instructor, description, amount):
    df = pd.read_csv("%s%s.csv" % (dc_totals_folder_path, instructor))
    df.drop(df.tail(1).index, inplace=True)
    df = df.append({'Amount_Due_To_Instructor': amount,
                    'Series_Used': description, 'Instructors': 'Adjustment'}, ignore_index=True)
    df = df.append({'Instructors': 'Total', 'Amount_Due_To_Instructor':
        df['Amount_Due_To_Instructor'].sum()}, ignore_index=True)
    if os.path.exists('%s%s.csv' % (dc_totals_folder_path, instructor)):
        os.remove('%s%s.csv' % (dc_totals_folder_path, instructor))
    df.to_csv("%s%s.csv" % (dc_totals_folder_path,
                            instructor), mode="w", index=False)


def clean_up_df_for_web(df):
    if "Rate" in df.columns:
        df = df.drop(columns=["Rate"])
    if "Instructor_Pay" in df.columns:
        df = df.drop(columns=["Instructor_Pay"])
    if "lower" in df.columns:
        df = df.drop(columns=["lower"])
    df.columns = [c.replace('_', ' ') for c in df.columns]
    df = df.fillna('')
    pd.options.display.float_format = '${:,.2f}'.format
    return df


def create_workspace():
    create_all_folders()
    with create_connection(database_path) as conn:
        wipe_instructors_database(conn)
        create_table(conn, config.sql_create_instructors_table)
        create_table(conn, config.sql_create_auth_code_table)


# writes html files to export_html_folder_path and pdf files to export_pdf_folder_path


def export_paystubs_to_pdf(selected_filenames):
    for file in os.listdir(dc_totals_folder_path):
        # Get the instructor ID from the file name
        # selected_filenames = file.split('.')[0]
        # Skip this file if the instructor is not in the selected list
        if file not in selected_filenames:
            continue
        output_html_file = dc_export_html_folder_path + \
                           file.replace('.csv', '') + '.html'
        output_pdf_file_name = dc_export_pdf_folder_path + get_global_pay_period() + '--' \
                               + file.replace('.csv', '') + '.pdf'
        input_file = dc_totals_folder_path + file
        df = pd.read_csv(input_file)
        df = clean_up_df_for_web(df)
        df.index += 1
        total = '${:,.2f}'.format(df.iloc[-1][-1])
        student_count = df['Instructors'].count() - 1
        create_html_paystub_file(file, str(total), str(student_count), get_global_pay_period()
                                 .replace('-', '/').replace('_/_', ' - '))
        add_table_to_html_paystub_file(df.to_html(classes="table table-striped table-hover table-sm table-responsive"),
                                       output_html_file)
        # added below line to fix export feature
        # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        # pdfkit.from_file(output_html_file, output_pdf_file_name, configuration=config)
        if sys.platform == 'win32':
            wk = subprocess.check_output('where wkhtmltopdf')
        else:
            wk = '/usr/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=wk)
        pdfkit.from_file(output_html_file,
                         output_pdf_file_name, configuration=config)


def sort_name(val):
    return val[InstructorRecord.NAME]


def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {file_path}. Reason: {e}")


# finds any classes who's pricing options do not show up in the pricing options list
# writes them to output/unpaid folder
def dc_find_unpaid_classes(po_df, ipo_df, classes_path):
    df = pd.read_csv(output_folder_path +
                     data_cleaner_output_folder + classes_path)
    # df['lower'] = df.Series_Used.str.lower()
    po_df['lower'] = po_df.index
    ipo_df['lower'] = ipo_df.index
    df = pd.merge(df, po_df, left_on='Series_Used',
                  right_on='lower', how="outer", indicator=True)
    df = df[df['_merge'] == 'left_only']
    if "_merge" in df.columns:
        df = df.drop(columns=["_merge"])
    if "lower" in df.columns:
        df = df.drop(columns=["lower"])
    # Filter the df DataFrame based on Instructor Prices
    df = df[~df['Series_Used'].isin(ipo_df.index)]

    pricing_option_dfs = dict(tuple(df.groupby('Series_Used')))
    for pricing_option in pricing_option_dfs:
        pricing_option_dfs[pricing_option].to_csv("%s%s.csv" % (dc_unpaid_folder_path, pricing_option.replace(' ', '_')
                                                                .replace('/', '---')), mode='w', index=False)
    return pricing_option_dfs


def get_pay_period_from_filename(filename):
    pay_period = None
    dates = re.findall('\d{1,2}\-\d{1,2}\-\d{4}', filename)
    if len(dates) > 1:
        pay_period = dates[0] + '_-_' + dates[1]
    return pay_period


def set_global_pay_period(pay_period):
    f = open(output_folder_path + 'payperiod.txt', "w+")
    f.write(pay_period)
    f.close()


def get_global_pay_period():
    f = open(output_folder_path + 'payperiod.txt')
    return f.read()
