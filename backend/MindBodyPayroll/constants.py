from enum import IntEnum

dat_folder_path = "../dataProcessing/dat/"
tmp_folder_path = "../dataProcessing/tmp/"
log_folder_path = "../dataProcessing/log/"
raw_folder_path = "../dataProcessing/raw/"
data_cleaner_upload_folder_path = "../DataCleaner/uploads/"
uploads_folder_path = "./uploads/"
public_classes_folder_path = "../output/publicClasses/"
private_classes_folder_path = "../output/privateClasses/"
instructor_dance_folder_path = "../output/instructorDances/"
unpaid_folder_path = "../output/unpaid/"
pricing_options_path = "../lookupTables/pricing-options.csv"
class_name_lookup_path = "../lookupTables/class-name-lookup.csv"
all_classes_path = "00-01-Class-All.csv"
all_private_classes_path = "00-02-Private-All.csv"
totals_folder_path = "../output/totals/"
output_folder_path = "../output/"
export_folder_path = "../output/export/"
export_html_folder_path = "../output/export/html/"
export_pdf_folder_path = "../output/export/pdf/"
logo_path = "static/img/logo.txt"
database_path = "db/payroll.db"
data_cleaner_output_folder = "data_cleaner_output/"



class InstructorRecord(IntEnum):
    ID = 0
    NAME = 1
    TOTAL = 2
