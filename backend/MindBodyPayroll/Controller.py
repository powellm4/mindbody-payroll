from functions import *
from flask import *
import os
import shutil
import pandas as pd
import numpy as np
import subprocess
from constants import *
from forms import AppendForm
from PyQt5.QtWidgets import *
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


app = Flask(__name__)
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
