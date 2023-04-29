from os.path import basename
from wrappers import *
from flask import *
import os
import datetime
import zipfile
import io
import pathlib
# import redis
#import authorization_service
import pandas as pd
from constants import *
from forms import AppendForm
from werkzeug.utils import secure_filename
from google_cloud_storage_service import GoogleCloudStorageService
from passlib.hash import argon2

# coding=latin-1

UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
ALLOWED_EXTENSIONS = set(['xls'])
cloud_storage = GoogleCloudStorageService()
cloud_storage.fetch_prices()
cloud_storage.fetch_classes()

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='carolina', password='$argon2id$v=19$m=102400,t=4,p=8$F0KIkXJO6R0D4FzLeQ9BCA$twGMgjibL08kIbZDqmggfg'))
users.append(User(id=2, username='antuanet', password='$argon2id$v=19$m=102400,t=4,p=8$4dzbuzcmBMDYG8NYK8WYsw$BgE4M4sdpOsSfDD1NJVkOQ'))
users.append(User(id=3, username='marshall', password='$argon2id$v=19$m=102400,t=4,p=8$1xpjbG3NWasVovSe0zrnvA$3f4lzCHokqOwQnSiO2VdKg'))
users.append(User(id=4, username='nuatu', password='$argon2id$v=19$m=102400,t=4,p=8$611L6f1/z/kfA6C01prTmg$PUC8YLJ4oZUra+Pxu9Cu9g'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
    # g is the application context where we're storing some data
    # since g lasts only the lifetime of the request, we reset it before every new request
    # see below doc for more info
    # https://flask.palletsprojects.com/en/1.1.x/appcontext/#storing-data
    print(g.user)
    print(session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        try:
            user = [x for x in users if x.username == username][0]
            if user and argon2.verify(password, user.password):# user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('upload_file'))
        except IndexError:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/')
def upload_form():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if not g.user:
        return redirect(url_for('login'))

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
            print(os.getcwd())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # calling run_backend in wrapper.py
            run_backend(filename)
            return redirect('/unpaid/')


@app.route('/paystubs/')
def paystubs():
    if not g.user:
        return redirect(url_for('login'))

    # paystub_list = os.listdir(totals_folder_path)
    with create_connection(database_path) as conn:
        instructors_tuples = select_all_instructors(conn)

    formatted_list = []
    for item in instructors_tuples:
        name = item[InstructorRecord.NAME]
        if os.path.exists('%s%s' % (dc_totals_folder_path, name)):
            df = pd.read_csv(dc_totals_folder_path +
                             item[InstructorRecord.NAME])
            total = '${:,.2f}'.format(df.iloc[-1][-1])

            # Format name as "Last, F"
            split_name = name.split(".")
            first_initial = split_name[0]
            last_name = split_name[-2]
            formatted_name = f"{last_name}, {first_initial}"

            formatted_list.append((item[InstructorRecord.ID], formatted_name, total))
    if not formatted_list:
        return redirect('/')

    def sort_by_last_name(item):
        full_name = item[1]
        last_name = full_name.split(",")[0]  # Extract the last name
        return last_name

    formatted_list.sort(key=sort_by_last_name)

    return render_template('paystubs/index.html', instructors_list=formatted_list,
                           len=len(formatted_list))


@app.route('/paystubs/<int:id>', methods=['POST', 'GET'])
def paystubs_detail(id):
    if not g.user:
        return redirect(url_for('login'))

    form = AppendForm(request.form)
    paystub_list = os.listdir(dc_totals_folder_path)

    if request.method == 'POST':
        amount = form.amount.data
        instructor = form.instructor.data
        description = form.description.data
        make_adjustment(instructor, description, amount)
        return redirect(url_for('paystubs_detail', id=id))
    else:
        with create_connection(database_path) as conn:
            form.instructor.data = select_instructor_by_id(
                conn, id)[InstructorRecord.NAME].replace('.csv', '')

    with create_connection(database_path) as conn:
        file_name = select_instructor_by_id(conn, id)[InstructorRecord.NAME]
    df = pd.read_csv(dc_totals_folder_path+file_name)
    df = clean_up_df_for_web(df)
    form.amount.data = ''
    form.description.data = ''
    form.total.data = '${:,.2f}'.format(df.iloc[-1][-1])

    return render_template('paystubs/detail.html', paystub=df.to_html(classes="table table-striped table-hover "
                                                                              "table-sm table-responsive"), form=form)


@app.route('/prices/',  methods=['POST', 'GET'])
def prices():
    if not g.user:
        return redirect(url_for('login'))

    cloud_storage = GoogleCloudStorageService()
    pd.set_option('display.max_colwidth', None)
    if request.method == 'POST':
        req_data = request.get_json()
        df = pd.DataFrame.from_dict(req_data)
        df = df[['Pricing Option', 'Revenue per class', 'Instructor Pay']]
        df.to_csv("%s" % pricing_options_path, index=False)
        cloud_storage.save_prices()
        dict = {"redirect": '/prices/'}
        return jsonify(dict)

    cloud_storage.fetch_prices()
    df = pd.read_csv(pricing_options_path)

    # Add an empty column for the "Remove" buttons
    df['Remove'] = ''

    # Render the table with the "Remove" button in each row
    table_html = df.to_html(classes="table table-striped table-hover table-sm", escape=False)
    table_html = table_html.replace('<td></td>', '<td><button class="btn btn-danger remove">Remove</button></td>')

    return render_template('prices/index.html', prices=table_html)

@app.route('/classes/',  methods=['POST', 'GET'])
def classes():
    if not g.user:
        return redirect(url_for('login'))

    cloud_storage = GoogleCloudStorageService()
    if request.method == 'POST':
        req_data = request.get_json()
        df = pd.DataFrame.from_dict(req_data)
        df = df[['Name', 'Day', 'Time', 'Class']]
        df.to_csv("%s" % class_name_lookup_path, index=False)
        cloud_storage.save_classes()
        dict = {"redirect": '/classes/'}
        return jsonify(dict)

    cloud_storage.fetch_classes()
    df = pd.read_csv(class_name_lookup_path)

    # Add an empty column for the "Remove" buttons
    df['Remove'] = ''

    # Render the table with the "Remove" button in each row
    table_html = df.to_html(classes="table table-striped table-hover table-sm", escape=False)
    table_html = table_html.replace('<td></td>', '<td><button class="btn btn-danger remove">Remove</button></td>')

    return render_template('classes/index.html', classes=table_html)


@app.route('/export/', methods=['POST'])
def export():
    if not g.user:
        return redirect(url_for('login'))
    # clear out pdfs from previous exports
    delete_all_files_in_folder(dc_export_pdf_folder_path)
    selected_filenames = request.form.getlist('instructor_filenames[]')
    selected_filenames = [filename.replace(',', '') for filename in selected_filenames]

    export_paystubs_to_pdf(selected_filenames)
    base_path = pathlib.Path(dc_export_pdf_folder_path)
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name, basename(f_name))
    data.seek(0)
    return send_file(
        data,
        max_age=-1,
        mimetype='application/zip',
        as_attachment=True,
        download_name=get_global_pay_period() + '.zip'
    )


@app.route('/unpaid/',  methods=['GET'])
def unpaid():
    if not g.user:
        return redirect(url_for('login'))

    tables = {}
    for file in os.listdir(dc_unpaid_folder_path):
        df = pd.read_csv(dc_unpaid_folder_path + file)
        df = clean_up_df_for_web(df)
        tables[file.replace('_', ' ').replace('---', '/').replace('.csv', '')
               ] = df.to_html(classes="table table-striped table-hover table-sm")
    return render_template('unpaid.html', tables=tables)


@app.route('/instructions/',  methods=['GET'])
def instructions():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('instructions.html')


""" @app.route('/quickbooks/auth',  methods=['GET'])
def authorize_quickbooks():
    return redirect(authorization_service.authorize_quickbooks()) """


""" @app.route('/oauth-redirect',  methods=['GET'])
def oauth_redirect():
    code = request.args.get('code')
    realm_id = request.args.get('realmId')

    # is it necessary to store auth code??
    with create_connection(database_path) as conn:
        update_auth_code(conn, code, realm_id)

    # make call for bearer token
    authorization_service.auth_client.get_bearer_token(code, realm_id=realm_id)

    # retrieve access_token and refresh_token
    print(authorization_service.auth_client.access_token)
    print(authorization_service.auth_client.refresh_token)

    # store with redis
    return redirect('/paystubs/') """


if __name__ == '__main__':
    create_workspace()
    app.run(debug=True)
