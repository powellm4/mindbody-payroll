from enum import IntEnum
from pathlib import Path


# python data_cleaner related folders
data_cleaner_output_folder = "data_cleaner_output/"
dc_classes_folder_path = "../output/dc_classes/"
dc_instructor_dance_folder_path = "../output/dc_instructor_dances/"
dc_unpaid_folder_path = "../output/dc_unpaid/"
dc_export_folder_path = "../output/dc_export/"
dc_export_html_folder_path = "../output/dc_export/html/"
dc_export_pdf_folder_path = "../output/dc_export/pdf/"
dc_totals_folder_path = "../output/dc_totals/"


# payroll outputs when using data cleaner scripts
all_classes_path = "00-01-Class-All.csv"
totals_folder_path = "../output/totals/"
export_folder_path = "../output/export/"
public_classes_folder_path = "../output/publicClasses/"
private_classes_folder_path = "../output/privateClasses/"
instructor_dance_folder_path = "../output/instructorDances/"
unpaid_folder_path = "../output/unpaid/"
export_html_folder_path = "../output/export/html/"
export_pdf_folder_path = "../output/export/pdf/"

# lookup tables
pricing_options_path = "../lookupTables/pricing-options.csv"
class_name_lookup_path = "../lookupTables/class-name-lookup.csv"


uploads_folder_path = "./uploads/"
output_folder_path = "../output/"


logo_path = "static/img/logo.txt"
database_path = Path("payroll.db")


# enums
class InstructorRecord(IntEnum):
    ID = 0
    NAME = 1
    TOTAL = 2


class AuthCodeRecord(IntEnum):
    ID = 0
    CODE = 1
    REALM_ID = 2
