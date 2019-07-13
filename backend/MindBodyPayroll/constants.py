from enum import IntEnum

dat_folder_path = "../dataProcessing/dat/"
tmp_folder_path = "../dataProcessing/tmp/"
log_folder_path = "../dataProcessing/log/"
raw_folder_path = "../dataProcessing/raw/"
uploads_folder_path = "./uploads/"
public_classes_folder_path = "../output/publicClasses/"
private_classes_folder_path = "../output/privateClasses/"
instructor_dance_folder_path = "../output/instructorDances/"
unpaid_folder_path = "../output/unpaid/"
pricing_options_path = "../lookupTables/pricing-options.csv"
class_name_lookup_path = "../lookupTables/class-name-lookup.csv"
all_classes_path = "00-01-Class-All.csv"
totals_folder_path = "../output/totals/"
output_folder_path = "../output/"
export_folder_path = "../output/export/"
export_html_folder_path = "../output/export/html/"
export_pdf_folder_path = "../output/export/pdf/"
logo_path = "static/img/logo.txt"
database_path = "db/payroll.db"


class InstructorRecord(IntEnum):
    ID = 0
    NAME = 1
    TOTAL = 2
