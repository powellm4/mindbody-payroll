from constants import export_html_folder_path, logo_path



def create_html_paystub_file(file, total, student_count, pay_period):
    output_html_file = export_html_folder_path + file.replace('.csv', '') + '.html'
    f = open(output_html_file, "w+")
    f.write(get_header(file, total, student_count, pay_period))
    f.write(get_styles())
    f.close()


def add_table_to_html_paystub_file(table, output_html_file):
    f = open(output_html_file, 'a')
    f.write(table)
    f.close()


def get_header(file, total, student_count, pay_period):
    return """
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <div class="row">
        <div class="column">
            <img src="data:image/png;base64,""" + get_vmac_logo() + """ " alt="VMAC Logo" />
        </div>
        <div class="column">
            <h3 class="text-right">Number of Students: """+student_count+"""</h3>
             <h3 class="text-right">Pay Date Range: """+pay_period+"""</h3>
        </div>
    </div>
    <div class="row">
        <div class="column">
            <h1>""" + file.replace('.csv', '') + """</h1>
        </div>
        <div class="column">
            <h1 class="text-right">Check Amount: """+total+"""</h1>
        </div>
    </div>"""


def get_vmac_logo():
    with open(logo_path) as f:
        return f.read()


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def get_styles():
    return """<style>
    
        .column {
          float: left;
          width: 50%;
        }
        
        /* Clear floats after the columns */
        .row:after {
          content: "";
          display: table;
          clear: both;
        }

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
            vertical-align: bottom;
        
        }
        .right span {
           position: absolute;
           bottom: 0;
           right: 0;
        }
        .container {
          width: 100%;
          padding-right: 15px;
          padding-left: 15px;
          margin-right: auto;
          margin-left: auto;
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
        
        .text-right {
          text-align: right !important;
          vertical-align: bottom;
        }
         
        </style>"""