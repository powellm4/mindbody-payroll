from functions import *
from flask import *
import os
import shutil
import pandas as pd
import numpy as np
import subprocess
from constants import *
from PyQt5.QtWidgets import *


app = Flask(__name__)
@app.route('/paystubs/')
def index():
    paystub_list = os.listdir(totals_folder_path)
    return render_template('paystubs/index.html', paystub_list=paystub_list, len=len(paystub_list))


@app.route('/paystubs/<int:id>')
def detail(id):
    paystub_list = os.listdir(totals_folder_path)
    file = paystub_list[id]
    df = pd.read_csv(totals_folder_path+paystub_list[id])
    return render_template('paystubs/detail.html', paystub=df.to_html())


if __name__ == '__main__':
      app.run(debug=True)