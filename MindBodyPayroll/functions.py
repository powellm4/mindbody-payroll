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


def write_instructor_to_csv(df, instructor):
    df['Instructors'] = instructor
    if os.path.isfile("%s%s.csv" % (output_folder, instructor)):
        mode = "a"
        include_header = False
        print("Found %s CSV, appending new data" % instructor)
    else:
        mode = "w"
        include_header = True
        print("Writing %s to new CSV..." % instructor)
    df.to_csv("%s%s.csv" % (output_folder, instructor), mode=mode, header=include_header, index=False)


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
#   all instructor classes to their own file
# inputs: input_folder - contains full data csv
#           pd_df - pricing lookup dataFrame
def export_instructor_dances(po_df):
    file = all_classes_file
    df = pd.read_csv("%s%s" % (input_folder, file))
    df = clean_up_dataframe(df, po_df)
    df = assign_instructor_rate(df)
    df = assign_amount_due(df)
    df = df[df.Series_Used == "VMAC INSTRUCTOR DANCE"]
    df.Amount_Due_To_Instructor = df.Amount_Due_To_Instructor * -1
    unique_instructors = df.Client_Name.unique()
    for instructor in unique_instructors:
        udf = df[df.Client_Name == instructor]
        write_to_instructor_dance_csv(udf, instructor)