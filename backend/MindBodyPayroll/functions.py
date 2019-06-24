import os
import shutil
import pandas as pd
import subprocess
import pdfkit
from constants import *
from shutil import copyfile
from sys import exit
from pdf_helper import create_html_paystub_file, add_table_to_html_paystub_file


# display floats as currency
pd.options.display.float_format = '{:,.2f}'.format


# display all columns for debugging
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1500)


# the main function for processing a list of classes
# makes calls to helper functions and outputs a csv for each instructor
def handle_classes(list_of_classes, po_df):
    # for each (public/private) class file in dataProcessing/dat/ folder
    for file in list_of_classes:
        df = pd.read_csv("%s%s" % (dat_folder_path, file))
        instructors_list = get_instructors_list(df)
        df = clean_up_dataframe(df, po_df)
        df = assign_instructor_rate(df, len(instructors_list))
        df = assign_amount_due(df)
        for instructor in instructors_list:
            write_instructor_to_csv(df, instructor, public_classes_folder_path)
            if "02-Private" in list_of_classes[0]:
                write_instructor_to_csv(df, instructor, private_classes_folder_path, provide_feedback=False)


# input: 'Instructors' cell from processed data
# output: Array of instructor(s), formatted as F.Last
def get_instructors_list(df):
    instructors_cell = df.loc[0, "Instructors"]
    if "&" in instructors_cell:
        instructors = instructors_cell.replace("&", "").strip().split(', ')
        for i in range(len(instructors)):
            # print(instructors[i])
            temp = instructors[i].split()
            last = temp[1]
            first = temp[0][0]
            full = first+"."+last
            instructors[i] = full
    else:
        instructors = [instructors_cell]
        for i in range(len(instructors)):
            # print(instructors[i])
            temp = instructors[i].split(', ')
            first = temp[1]
            first = first[0]
            last = temp[0].replace(",", "").replace(' ', '-').strip()
            full = first+"."+last
            instructors[i] = full
    # print(instructors)
    return instructors


# takes care of merging in the pricing options and
# making the dataframe easier to process
def clean_up_dataframe(df, po_df=None):
    if is_alternate_format(df):
        if ' "Class name"' in df.columns:
            df = reformat_alternate_public(df)
        else:
            df = reformat_alternate_private(df)
    df = format_column_headers(df)
    df = drop_unnecessary_columns(df)
    df = remove_quotes(df)
    if po_df is not None:
        df = include_pricing_options(df, po_df)
    df = format_client_name(df)
    df = sort_by_date_time(df)
    return df


# detects private classes that show up in a different format from mindbody
def is_alternate_format(df):
    if "# Clients" in df.columns or ' "# Clients"' in df.columns:
        return True


# fix for private classes coming in 2 separate formats
def correct_private_class_file(df):
    # df['Series_Used'] =
    return None


def drop_unnecessary_columns(df):
    if "Unnamed:_5" in df.columns:
        df = df.drop(columns=["Unnamed:_5"])
    if "Earnings_per_Client" in df.columns:
        df = df.drop(columns=["Earnings_per_Client"])
    if "Earnings" in df.columns:
        df = df.drop(columns=["Earnings"])
    if "Revenue" in df.columns:
        df = df.drop(columns=["Revenue"])
    if "Rev_per_Session" in df.columns:
        df = df.drop(columns=["Rev_per_Session"])
    return df


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
        return first+'.'+last
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
    df = df.assign(Amount_Due_To_Instructor=(df.Instructor_Pay.astype(float) * df.Rate).round(3))
    return df


# takes a client name in F Last format
# returns name in F.Last format
def format_client_name(df):
    df.Client_Name = df.Client_Name.str.replace(" ", "")
    return df


# sorts a dataframe by class date, class time
def sort_by_date_time(df):
    df.Class_Date = pd.to_datetime(df.Class_Date)
    return df.sort_values(by=['Class_Date', 'Class_Time'])


# decides whether an instructors csv already exists,
# writing to a new csv if not
# appending to existing csv if so
# provide_feedback allows you to turn off print statements
def write_instructor_to_csv(df, instructor, output_folder, provide_feedback=True, instructor_dance=False):
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
    df.to_csv("%s%s.csv" % (output_folder, instructor), mode=mode, header=include_header, index=False)


# prepares the class name lookup dataframe for
# merging into main df
def clean_up_class_name_dataframe(cn_df):
    cn_df = format_column_headers(cn_df)
    cn_df.Day = cn_df.Day.map(dict(Mondays=0, Tuesdays=1, Wednesdays=2, Thursdays=3, Fridays=4, Saturdays=5, Sundays=6))
    cn_df.Name = cn_df.Name.apply(format_name)
    cn_df.Time = cn_df.Time.str.replace("PM", "pm")
    cn_df.Time = cn_df.Time.str.replace("AM", "am")
    return cn_df


# merges the dataFrame with the pricing options dataFrame to allow lookup of pricing options
def include_pricing_options(df, po_df):
    # if "#_Clients" in df.columns:
    return pd.merge(df, po_df, left_on='Series_Used', right_on='Pricing_Option', how='left')


# merges the class name lookup dataframe with the main dataframe,
# adds; the class column
def include_class_names(df, cn_df):
    df['Day'] = pd.to_datetime(df.Class_Date).dt.dayofweek
    merged_df = pd.merge(df, cn_df, left_on=['Day', 'Instructors', 'Class_Time'],
                   right_on=['Day', 'Name', 'Time'], how='left')
    merged_df = merged_df.drop(columns=['Day', 'Name', 'Time'])
    merged_df = merged_df[['Instructors', 'Class', 'Class_Date', 'Class_Time',
                           'Client_Name', 'Series_Used', 'Revenue_per_class',
                           'Instructor_Pay', 'Rate', 'Amount_Due_To_Instructor']]
    return merged_df


# removes all quotes surround all data in dataFrame
def remove_quotes(df):
    df = df.apply(lambda x: x.str.strip())
    return df.apply(lambda x: x.str.strip('"'))


# takes the original dataFrame with all classes and writes
#   all instructor dances to their own file
# inputs: dat_folder - contains full data csv
#           pd_df - pricing lookup dataFrame
def export_instructor_dances(po_df):
    file = all_classes_path
    #

    #
    df = pd.read_csv("%s%s" % (dat_folder_path, file), error_bad_lines=False)
    df = clean_up_dataframe(df, po_df)
    df = assign_instructor_rate(df)
    df = assign_amount_due(df)
    df = df[(df.Series_Used == "VMAC INSTRUCTOR DANCE") | (df.Series_Used == "VMAC INSTRUCTOR FITNESS")]
    df = filter_out_jamal_carolina_classes(df)
    df.Amount_Due_To_Instructor = df.Amount_Due_To_Instructor * -2
    unique_instructors = df.Client_Name.unique()
    for instructor in unique_instructors:
        udf = df[df.Client_Name == instructor]
        write_instructor_to_csv(udf, instructor, instructor_dance_folder_path, instructor_dance=True)


# instructors get free classes if the class is taught by carolina and jamal
# removed all classes taught by carolina and or jamal from dataframe
def filter_out_jamal_carolina_classes(df):
    return df[~df.Instructors.str.contains('Jamal|Carolina', case=False, regex=True)]


# adds deduction rows to the files found in publicClasses folder
def append_instructor_dances():
    instructor_csv_list = [name for name in os.listdir(public_classes_folder_path)]
    instructor_dance_list = [name for name in os.listdir(instructor_dance_folder_path)]
    for file in instructor_csv_list:
        if file in instructor_dance_list:
            iddf = pd.read_csv('%s%s' % (instructor_dance_folder_path, file))
            print("appending %s " % file)
            iddf.to_csv("%s%s" % (public_classes_folder_path, file), mode="a", index=False, header=False)

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
def output_instructor_totals(cn_df):
    for file in os.listdir(public_classes_folder_path):
        print('Creating pay stub for %s' % file.replace('.csv', ''))
        df = pd.read_csv("%s%s" % (public_classes_folder_path, file))
        df = df.append(df.sum(numeric_only=True), ignore_index=True)
        df.iloc[-1][0] = 'Total'
        df = include_class_names(df, cn_df)

        df.to_csv("%s%s" % (totals_folder_path, file), mode="w", index=False)


# same as running the shell command:
# rm -f ./dat/* ./tmp/* ./log/*
def clean_up_dataProcessing_folder():
      for file in os.listdir(dat_folder_path):
            os.remove(dat_folder_path + file)
      for file in os.listdir(tmp_folder_path):
            os.remove(tmp_folder_path + file)
      for file in os.listdir(log_folder_path):
            os.remove(log_folder_path + file)


# removes any data generated by previous runs
def clean_up_workspace():
    if os.path.isdir(output_folder_path):
        shutil.rmtree(output_folder_path)


# move uploaded file to raw_folder_path 
# where dataprocessing looks for it
def move_uploaded_file(filename):
    source = uploads_folder_path + filename
    target = raw_folder_path + filename
    # adding exception handling
    try:
        copyfile(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

    print("\nFile copy done!\n")


# reads in pricing lookup table &
# prepares it for processing and merging
def get_pricing_option_lookup_df():
    po_df = pd.read_csv(pricing_options_path)
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


# gets list of file names from the dat folder
def get_list_of_classes(public=False, private=False):
    if public:
        prefix = "01-Class"
    if private:
        prefix = "02-Private"
    return [name for name in os.listdir(dat_folder_path) if name.startswith(prefix)]


# opens file in totals folder, adds adjustment, recalculates total and rewrites file
# input - description - is added under the Series_Used column
def make_adjustment(instructor, description, amount):
    df = pd.read_csv("%s%s.csv" % (totals_folder_path, instructor))
    df.drop(df.tail(1).index, inplace=True)
    df = df.append({'Amount_Due_To_Instructor': amount,
                    'Series_Used': description, 'Instructors': 'Adjustment'}, ignore_index=True)
    df = df.append({'Instructors': 'Total', 'Amount_Due_To_Instructor': df['Amount_Due_To_Instructor'].sum()}, ignore_index=True)
    if os.path.exists('%s%s.csv' % (totals_folder_path, instructor)):
        os.remove('%s%s.csv' % (totals_folder_path, instructor))
    df.to_csv("%s%s.csv" % (totals_folder_path, instructor), mode="w", index=False)


# takes a file and runs all of the shell scripts with it
# input - path to file
def run_data_processing_shell_scripts(dir_plus_filename):
    os.chdir('../dataProcessing')
    subprocess.run(['./bin/s00-generate_csv_files.sh', dir_plus_filename])
    os.chdir('../MindBodyPayroll')
    subprocess.run(['pwd'])


def clean_up_df_for_web(df):
    if "Rate" in df.columns:
        df = df.drop(columns=["Rate"])
    if "Instructor_Pay" in df.columns:
        df = df.drop(columns=["Instructor_Pay"])
    df.columns = [c.replace('_', ' ') for c in df.columns]
    df = df.fillna('')
    # safe to take out next line
    df.iloc[-1][0] = 'Total'
    pd.options.display.float_format = '${:,.2f}'.format
    return df


# writes html files to export_html_folder_path and pdf files to export_pdf_folder_path
def export_paystubs_to_pdf():
    for file in os.listdir(totals_folder_path):
    # for file in ["D.McKnight.csv"]: # for testing purposes only
        output_html_file = export_html_folder_path + file.replace('.csv', '') + '.html'
        output_pdf_file = export_pdf_folder_path + file.replace('.csv', '') + '.pdf'

        input_file = totals_folder_path + file
        df = pd.read_csv(input_file)
        df = clean_up_df_for_web(df)
        total = '${:,.2f}'.format(df.iloc[-1][-1])

        create_html_paystub_file(file, str(total))
        add_table_to_html_paystub_file(df.to_html(classes="table table-striped table-hover table-sm table-responsive"),
                                       output_html_file)

        pdfkit.from_file(output_html_file, output_pdf_file)


# corrects private class files that come in the wrong format
# attaches the 'private lesson' rate to all classes
def reformat_alternate_private(df):
    df.columns = [c.replace('"', '') for c in df.columns]
    df.columns = [c.strip() for c in df.columns]
    drop_list = ["Class Name", "# Clients", "# Comps", "Base Pay", "Earnings", "Assistant Pay", "Bonus Pay"]
    for column in drop_list:
        if column in df.columns:
            df = df.drop(columns=[column])

    df = df.rename(columns={'Client Name(s)': 'Client Name'})
    df['Series Used'] = "Private Lesson"
    df['Revenue'] = '0.00'
    df['Earnings'] = '0.00'
    return df


# reformats a file that comes in the wrong format from mindbody
def reformat_alternate_public(df):
    df.columns = [c.replace('"', '') for c in df.columns]
    df.columns = [c.strip() for c in df.columns]

    if "Client Name(s)" in df.columns:
        df = df.rename(columns={"Client Name(s)": "Client Name"})
    elif "Client Name" not in df.columns:
        df["Client Name"] = ''

    df["Series Used"] = df["Class name"]
    drop_list = ['Class name', '# Clients', '# Comps', 'Base Pay', 'Assistant Pay', 'Bonus Pay']
    for column in drop_list:
        if column in df.columns:
            df = df.drop(columns=[column])

    df["Revenue"] = "0.00"
    df["Earnings"] = "0.00"
    return df


# finds any classes who's pricing options do not show up in the pricing options list
# writes them to output/unpaid folder
def find_unpaid_classes(po_df):
    df = pd.read_csv(dat_folder_path + all_classes_path)
    df = clean_up_dataframe(df)
    df = pd.merge(df, po_df, left_on='Series_Used', right_on='Pricing_Option', how="outer", indicator=True)
    df = df[df['_merge'] == 'left_only']
    if "_merge" in df.columns:
        df = df.drop(columns=["_merge"])

    pricing_option_dfs = dict(tuple(df.groupby('Series_Used')))
    for pricing_option in pricing_option_dfs:
        pricing_option_dfs[pricing_option].to_csv("%s%s.csv" % (unpaid_folder_path, pricing_option.replace(' ', '_')
                                                                .replace('/','---')), mode='w', index=False)
    return pricing_option_dfs
