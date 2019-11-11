sql_create_instructors_table = """ CREATE TABLE IF NOT EXISTS instructors (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        total text
                                    ); """

unnecessary_columns = ["Unnamed:_5", "Earnings_per_Client", "Earnings", "Revenue", "Rev_per_Session"]
UPLOAD_FOLDER = './uploads/'