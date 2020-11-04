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


unnecessary_columns = ["Unnamed:_5", "Earnings_per_Client",
                       "Earnings", "Revenue", "Rev_per_Session"]
UPLOAD_FOLDER = './uploads/'


quickbooks_redirect_uri = "http://localhost:56733/oauth-redirect"
quickbooks_oauth2_base_uri = "https://appcenter.intuit.com/connect/oauth2"

# Google Cloud Storage
google_storage_cred_file = 'vmac-1-6a2f92d95ce4.json'
google_bucket_name = "vmac-mindbody-data"
prices_blob_name = "Prices/pricing-options.csv"
classes_blob_name = "Classes/class-name-lookup.csv"
