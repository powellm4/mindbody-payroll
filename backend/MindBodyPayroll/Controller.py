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
            print(filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # calling run_backend in wrapper.py
            run_backend(filename)
            return redirect('/paystubs/')


@app.route('/paystubs/')
def paystubs():
    paystub_list = os.listdir(totals_folder_path)
    totals_list = []
    for file in paystub_list:
        df = pd.read_csv(totals_folder_path + file)
        totals_list.append('${:,.2f}'.format(df.iloc[-1][-1]))

    return render_template('paystubs/index.html', totals_list=totals_list,
                           paystub_list=paystub_list, len=len(paystub_list))


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


@app.route('/prices/',  methods=['POST', 'GET'])
def prices():
    pd.set_option('display.max_colwidth', -1)
    if request.method == 'POST':
        req_data = request.get_json()
        df = pd.DataFrame.from_dict(req_data)
        df = df[['Pricing Option', 'Revenue per class', 'Instructor Pay']]
        df.to_csv("%s" % pricing_options_path, index=False)
        dict = {"redirect": '/prices/'}
        return jsonify(dict)

    df = pd.read_csv(pricing_options_path)

    return render_template('prices/index.html', prices=df.to_html(classes="table table-striped table-hover table-sm"))


@app.route('/classes/',  methods=['POST', 'GET'])
def classes():
    if request.method == 'POST':
        req_data = request.get_json()
        df = pd.DataFrame.from_dict(req_data)
        df = df[['Name', 'Day', 'Time', 'Class']]
        df.to_csv("%s" % class_name_lookup_path, index=False)
        dict = {"redirect": '/classes/'}
        return jsonify(dict)

    df = pd.read_csv(class_name_lookup_path)
    return render_template('classes/index.html', classes=df.to_html(classes="table table-striped table-hover table-sm"))


@app.route('/export/', methods=['POST', 'GET'])
def export():
    export_paystubs_to_pdf()
    base_path = pathlib.Path(export_pdf_folder_path)
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)
    return send_file(
        data,
        cache_timeout=-1,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=get_global_pay_period() + '.zip'
    )


@app.route('/unpaid/',  methods=['GET'])
def unpaid():
    tables = {}
    for file in os.listdir(unpaid_folder_path):
        df = pd.read_csv(unpaid_folder_path + file)
        df = clean_up_df_for_web(df)
        tables[file.replace('_', ' ').replace('---', '/').replace('.csv', '')] = df.to_html(classes="table table-striped table-hover table-sm")
        # from re import sub
        # import jinja2
        # environment = jinja2.Environment()
        # environment.filters['sub'] = sub
    return render_template('unpaid.html', tables=tables)


@app.route('/instructions/',  methods=['GET'])
def instructions():
    return render_template('instructions.html')


if __name__ == '__main__':
      app.run(debug=True)
