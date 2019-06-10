from functions import *
from wrappers import *
from flask import *
import os
import datetime
import zipfile
import io
import pathlib

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

            # prepend filename with upload time
            filename = secure_filename(file.filename)
            currentDT = datetime.datetime.now()
            filename = currentDT.strftime("%Y-%m-%d-%H-%M-%S") + '-' + filename
            print (filename)            

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            flash('Starting dataprocessing')

            # calling run_backend in wrapper.py
            run_backend(filename)
            return redirect('/')


@app.route('/paystubs/')
def paystubs():
    paystub_list = os.listdir(totals_folder_path)
    return render_template('paystubs/index.html', paystub_list=paystub_list, len=len(paystub_list))


@app.route('/paystubs/<int:id>', methods=['POST', 'GET'])
def paystubs_detail(id):
    form = AppendForm(request.form)
    paystub_list = os.listdir(totals_folder_path)

    if request.method == 'POST':
        amount = form.amount.data
        instructor = form.instructor.data
        description = form.description.data
        make_adjustment(instructor, description, amount)
        return redirect(url_for('paystubs_detail', id=id))
    else:
        form.instructor.data = paystub_list[id].replace('.csv', '')

    df = pd.read_csv(totals_folder_path+paystub_list[id])
    df = clean_up_df_for_web(df)
    form.amount.data = ''
    form.description.data = ''
    form.total.data = '${:,.2f}'.format(df.iloc[-1][-1])

    return render_template('paystubs/detail.html', paystub=df.to_html(classes="table table-striped table-hover "
                                                                              "table-sm table-responsive"), form=form)

@app.route('/prices/')
def prices():
    df = pd.read_csv(pricing_options_path)
    return render_template('prices/index.html', prices=df.to_html(classes="table table-striped table-hover table-sm"))


@app.route('/prices2/')
def prices2():
    df = pd.read_csv(pricing_options_path2)
    return render_template('prices/index.html', prices=df.to_html(classes="table table-striped table-hover table-sm table-responsive"))


@app.route('/prices/test', methods=['POST'])
def prices_test():
    # requests.get(url).json()
    req_data = request.get_json()
    df = pd.DataFrame.from_dict(req_data)
    df = df[['Pricing Option', 'Revenue per class', 'Instructor Pay']]
    df.to_csv("%s" % pricing_options_path2, index=False)
    dict = {"redirect": '/prices2/'}
    return jsonify(dict)


@app.route('/export/', methods=['POST', 'GET'])
def export():
    base_path = pathlib.Path(totals_folder_path)
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='latest-payroll.zip'
    )


if __name__ == '__main__':
      app.run(debug=True)
