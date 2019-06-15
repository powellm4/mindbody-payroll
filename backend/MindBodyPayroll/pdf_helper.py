from constants import export_html_folder_path


def create_html_paystub_file(file, total):
    output_html_file = export_html_folder_path + file.replace('.csv', '') + '.html'
    f = open(output_html_file, "w+")
    f.write(get_header(file, total))
    f.write(get_styles())
    f.close()


def add_table_to_html_paystub_file(table, output_html_file):
    f = open(output_html_file, 'a')
    f.write(table)
    f.close()


def get_header(file, total):
    return """<div ">
    <div class="left">
        <h1>""" + file.replace('.csv', '') + """</h1>
    </div>
    <div class="right">
        <h1 class="align-right">Total: """+total+"""</h1>
    </div>
    </div>"""


def get_styles():
    return """<style>
        table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 1rem;
        background-color: transparent;
        }
        
        .left{
        float: left;
        }
        .right{
        float: right;
        }
        
        .table th,
        .table td {
        padding: 0.75rem;
        vertical-align: top;
        border-top: 1px solid #dee2e6;
        }
        
        .table thead th {
        vertical-align: bottom;
        border-bottom: 2px solid #dee2e6;
        }
        
        .table tbody + tbody {
        border-top: 2px solid #dee2e6;
        }
        
        .table .table {
        background-color: #fff;
        }
        
        .table-striped tbody tr:nth-of-type(odd) {
        background-color: rgba(0, 0, 0, 0.05);
        }
        
        .table-sm th,
        .table-sm td {
        padding: 0.3rem;
        }
        
        
        </style>"""