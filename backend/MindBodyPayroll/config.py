sql_create_instructors_table = """ CREATE TABLE IF NOT EXISTS instructors (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        total text
                                    ); """