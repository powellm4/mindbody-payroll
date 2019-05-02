import os
import pandas as pd
from constants import *


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
            temp = instructors[i].split()
            first = temp[1]
            first = first[0]
            last = temp[0].replace(",", "").strip()
            full = first+"."+last
            instructors[i] = full
    # print(instructors)
    return instructors


def clean_up_dataframe(df, po_df):
    df = format_column_headers(df)
    df = drop_unnecessary_columns(df)
    df = remove_quotes(df)
    df = include_pricing_options(df, po_df)
    df = format_client_name(df)
    df = sort_by_date_time(df)
    return df


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
    return df


def create_folder(folder):
    if not os.path.exists('../output/'):
        os.mkdir('../output/')
    if not os.path.exists(folder):
        os.mkdir(folder)


def assign_amount_due(df):
    df.Instructor_Pay = df.Instructor_Pay.str.replace("$", "")
    return df.assign(Amount_Due_To_Instructor=df.Instructor_Pay.astype('float64') * df.Rate)


def format_client_name(df):
    df.Client_Name = df.Client_Name.str.replace(" ", "")
    return df


def sort_by_date_time(df):
    df.Class_Date = pd.to_datetime(df.Class_Date)
    return df.sort_values(by=['Class_Date', 'Class_Time'])


def write_instructor_to_csv(df, instructor):
    df['Instructors'] = instructor
    if os.path.isfile("%s%s.csv" % (public_classes_folder, instructor)):
        mode = "a"
        include_header = False
        print("Found %s CSV, appending new data" % instructor)
    else:
        mode = "w"
        include_header = True
        print("Writing %s to new CSV..." % instructor)
    df.to_csv("%s%s.csv" % (public_classes_folder, instructor), mode=mode, header=include_header, index=False)


# takes a dataFrame, isolates the instructor dances, and writes them to the master csv for instructor dances
def write_to_instructor_dance_csv(df, name):
    if os.path.isfile(instructor_dance_folder+name):
        mode = "a"
        include_header = False
    else:
        mode = "w"
        include_header = True
    df.to_csv("%s%s.csv" % (instructor_dance_folder, name), mode=mode, header=include_header, index=False)


# merges the dataFrame with the pricing options dataFrame to allow lookup of pricing options
def include_pricing_options(df, po_df):
    return pd.merge(df, po_df, left_on='Series_Used', right_on='Pricing_Option', how='left')


# removes all quotes surround all data in dataFrame
def remove_quotes(df):
    df = df.apply(lambda x: x.str.strip())
    return df.apply(lambda x: x.str.strip('"'))


# takes the original dataFrame with all classes and writes
#   all instructor dances to their own file
# inputs: input_folder - contains full data csv
#           pd_df - pricing lookup dataFrame
def export_instructor_dances(po_df):
    file = all_classes_path
    df = pd.read_csv("%s%s" % (input_folder, file))
    df = clean_up_dataframe(df, po_df)
    df = assign_instructor_rate(df)
    df = assign_amount_due(df)
    df = df[df.Series_Used == "VMAC INSTRUCTOR DANCE"]
    df = filter_out_jamal_carolina_classes(df)
    df.Amount_Due_To_Instructor = df.Amount_Due_To_Instructor * -1
    unique_instructors = df.Client_Name.unique()
    for instructor in unique_instructors:
        udf = df[df.Client_Name == instructor]
        write_to_instructor_dance_csv(udf, instructor)


# instructors get free classes if the class is taught by carolina and jamal
# removed all classes taught by carolina and or jamal from dataframe
def filter_out_jamal_carolina_classes(df):
    return df[~df.Instructors.str.contains('Jamal|Carolina', case=False, regex=True)]


# adds deduction rows to the files found in publicClasses folder
def append_instructor_dances():
    instructor_csv_list = [name for name in os.listdir(public_classes_folder)]
    instructor_dance_list = [name for name in os.listdir(instructor_dance_folder)]
    for file in instructor_csv_list:
        if file in instructor_dance_list:
            iddf = pd.read_csv('%s%s' % (instructor_dance_folder, file))
            print("appending %s " % file)
            iddf.to_csv("%s%s" % (public_classes_folder, file), mode="a", index=False, header=False)

    print("\n\nList of Instructor dances with no matching instructor CSV\n----------")
    for file in instructor_dance_list:
        if file not in instructor_csv_list:
            print('Instructor Dance: %s not found as an Instructor for pay period' % file)
            # name = file.replace(".csv", "")
            # check_against_family_lookup(name)


# given a name, check the family lookup table to see if
# the person is associated with an instructor
def check_against_family_lookup(name):
    fdf = pd.read_csv(instructor_family_lookup_path)
    fdf = fdf[fdf.Student == name]
    # instructor = fdf.Instructor
    print(fdf.head())


# writes csv to totals folder containing total for instructor
def output_instructor_totals():
    for file in os.listdir(public_classes_folder):
        df = pd.read_csv("%s%s" % (public_classes_folder, file))
        df = df.append(df.sum(numeric_only=True), ignore_index=True)
        df.to_csv("%s%s" % (totals_folder, file), mode="w", index=False)
