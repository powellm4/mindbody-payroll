# mindbody-payroll
Local dev environment setup

Clone:
https://github.com/powellm4/mindbody-payroll

Install:
Python 3.6 (optional if running via docker)
Docker

Before Build:
Go to google drive (https://drive.google.com/drive/folders/1W4wussqNYQIc5wL_YZvyho0Z4QllZLcH)
Download the vmac-1-xxxxxx.json file and place it into src/secrets/ folder (you will need to create the secrets folder
In the google_storage_service.py file, uncomment this line:
storage_client = storage.Client.from_service_account_json(google_storage_cred_file)
In the same file, comment out this line:
storage_client = storage.Client()
This is only for local config, dont push these changes

Build:
Docker-compose build

Run:
Docker-compose up
Using a browser other than Chrome, go to http://localhost:56733/
Chrome forces https, which is not set up locally. Chrome will not work.
Firefox recommended
