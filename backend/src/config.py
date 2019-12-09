sql_create_instructors_table = """ CREATE TABLE IF NOT EXISTS instructors (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        total text
                                    ); """

sql_create_auth_code_table = """ CREATE TABLE IF NOT EXISTS auth_code (
                                        id integer PRIMARY KEY,
                                        code text NOT NULL,
                                        realmId integer NOT NULL
                                    ); """


unnecessary_columns = ["Unnamed:_5", "Earnings_per_Client", "Earnings", "Revenue", "Rev_per_Session"]
UPLOAD_FOLDER = './uploads/'
client_id = "ABMcKd7PptrCHwrim3HlyboAAVrUbj3VIxQDCf5b4VMnbRJrwB"

client_secret = "ifuRNynQSfPwEm9YnxhgSy5gjq1wqO88P7A3uJcZ"

quickbooks_redirect_uri = "http://localhost:56733/oauth-redirect"
quickbooks_oauth2_base_uri = "https://appcenter.intuit.com/connect/oauth2"