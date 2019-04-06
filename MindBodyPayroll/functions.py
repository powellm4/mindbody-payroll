import os

# input: 'Instructors' cell from processed data
# output: Array of instructor(s)
def get_instructors_list(df):
    instructorsCell = df.loc[0,"Instructors"]
    if "&" in instructorsCell:
        instructors = instructorsCell.replace("&", "").strip().split(', ')
    else:
        instructors = [instructorsCell]
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
    return df
    
def assign_instructor_rate(df, no_of_instructors):
    return df.assign(Rate=0.5/no_of_instructors)

def format_column_headers(df):
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df.columns = [c.replace('.', '') for c in df.columns]
    return df

def create_output_folder(outputFolder):
    print('Creating folder All_Instructors_CSVs for program output...')
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    else:
        print('Folder already exists. Continuing...\n')

def assign_amount_due(df):
    df.Rev_per_Session = df.Rev_per_Session.str.replace("$","")
    return df.assign(Amount_Due_To_Instructor=df.Rev_per_Session.astype('float64')*df.Rate)

#configure file appending
def write_to_new_csv(df, instructorsList, outputFolder):
    for instructor in instructorsList:
        df['Instructors'] = instructor
        if os.path.isfile("%s%s.csv" % (outputFolder,instructor)):
            mode = "a"
            print("Found %s CSV, appending new data" % instructor)
        else:
            mode = "w"
            print("Writing %s to new CSV..." % instructor)
        df.to_csv("%s%s.csv" % (outputFolder,instructor), mode=mode)