from functions import *
from flask import *
import os
import pandas as pd
from constants import *
from forms import AppendForm
import urllib.request
from app import app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['xls'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Must be an xls file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            flash('Starting dataprocessing')
            # calling scripts
            file_name = filename
            print("\n------------------------------\n\n"
                  "\t   MindBody Payroll\n"
                  "\n------------------------------\n\n")

            # remove any output data from previous runs
            # clean_up_dataProcessing_folder()
            clean_up_workspace()
            create_all_folders()

            return redirect('/')


@app.route('/download')
def download_file():
    url = 'https://codeload.github.com/fogleman/Minecraft/zip/master'
    response = urllib.request.urlopen(url)
    data = response.read()
    response.close()



@app.route('/paystubs/')
def index():
    paystub_list = os.listdir(totals_folder_path)
    return render_template('paystubs/index.html', paystub_list=paystub_list, len=len(paystub_list))


@app.route('/paystubs/<int:id>', methods=['POST', 'GET'])
def detail(id):
    form = AppendForm(request.form)
    paystub_list = os.listdir(totals_folder_path)

    if request.method == 'POST':
        amount = form.amount.data
        instructor = form.instructor.data
        description = form.description.data
        make_adjustment(instructor, description, amount)
    else:

        form.instructor.data = paystub_list[id].replace('.csv', '')

    df = pd.read_csv(totals_folder_path+paystub_list[id])

    return render_template('paystubs/detail.html', paystub=df.to_html(), form=form)


if __name__ == '__main__':
      app.run(debug=True)
