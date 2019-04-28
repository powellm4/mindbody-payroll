import os
import pandas as pd


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


def assign_instructor_rate(df, no_of_instructors):
    return df.assign(Rate=1.0 / no_of_instructors)


def format_column_headers(df):
    df.columns = [c.strip() for c in df.columns]
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df.columns = [c.replace('.', '') for c in df.columns]
    df.columns = [c.replace('"', '') for c in df.columns]
    return df


def create_output_folder(output_folder):
    print('Creating folder All_Instructors_CSVs for program output...')
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    else:
        print('Folder already exists. Continuing...\n')


def assign_amount_due(df):
    df.Instructor_Pay = df.Instructor_Pay.str.replace("$", "")
    return df.assign(Amount_Due_To_Instructor=df.Instructor_Pay.astype('float64') * df.Rate)


def write_to_csv(df, instructors_list, output_folder):
    for instructor in instructors_list:
        df['Instructors'] = instructor
        if os.path.isfile("%s%s.csv" % (output_folder, instructor)):
            mode = "a"
            include_header = False
            print("Found %s CSV, appending new data" % instructor)
        else:
            mode = "w"
            include_header = True
            print("Writing %s to new CSV..." % instructor)
        df.to_csv("%s%s.csv" % (output_folder, instructor), mode=mode, header=include_header)


#merges the dataframe with the pricing options dataframe to allow lookup of pricing options
def include_pricing_options(df, po_df):
    return pd.merge(df, po_df, left_on='Series_Used', right_on='Pricing_Option', how='left')


#removes all quotes surround all data in dataframe
def remove_quotes(df):
    df = df.apply(lambda x: x.str.strip())
    return df.apply(lambda x: x.str.strip('"'))
