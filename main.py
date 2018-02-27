import os, sys
from flask import Flask, render_template, request,jsonify, g, redirect
from werkzeug.utils import secure_filename
import sqlite3
import datetime as dt
from gsutil.gs_operation import gs_add, gs_rm
from goodtables import validate


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/NXie/PycharmProjects/flask_google_uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['csv', 'xlsx'])
app.config['DATABASE'] = 'C:/Users/NXie/PycharmProjects/flask_google_uploads/files.db'
app.config.from_object(__name__)
# app.config.update({
#     "STORAGE_PROVIDER": "GOOGLE_STORAGE",
#     "STORAGE_CONTAINER": "neallab/dtp_reports/",
#     "STORAGE_KEY": "404444449189-54rf2ke9km6ml5aek9rkvl39mdanjc7l.apps.googleusercontent.com",
#     "STORAGE_SECRET": "8R-DCpcsS7FLNf94ACY0suwq"
# })

# storage = Storage()
# storage.init_app(app)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


def add_file(filename, label):
    query = 'insert or replace into fileinfo (filename, label) values (?, ?)'
    print (query)
    get_db().execute(query, [filename, label])
    get_db().commit()

def delete_file(filename):
    query = 'delete from fileinfo where filename = (?)'
    get_db().execute(query, [filename])
    get_db().commit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('file')
        label = dt.datetime.now().strftime("%a, %d. %B %Y %H:%M")
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                report = validate(os.path.join(app.config['UPLOAD_FOLDER'],filename), schema="C:/Users/NXie/PycharmProjects/flask_google_uploads/diagnostic/schema.json", order_fields=True)
                if report['valid']:
                    add_file(filename, label)
                    gs_add(filename)
                    return jsonify({'success': 'well done'})
                else:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return jsonify({'fail': report['tables'][0]['errors'][0]['message']})
            else:
                return jsonify({'fail': 'Your file extension is {}'.format(file.filename.rsplit('.', 1)[1].lower())})
    else:
        return render_template('index.html')

@app.route('/database')
def show_file():
    query = 'select filename, label from fileinfo'
    cursor = get_db().execute(query)
    items = cursor.fetchall()
    return jsonify({'data': items})

@app.route('/delete/<filename>', methods=['GET', 'POST'])
def remove_file(filename):
    query = 'delete from fileinfo where filename = ?'
    get_db().execute(query, [filename])
    get_db().commit()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    gs_rm(filename)
    return('Delete Success')

if __name__ == '__main__':
    app.run(debug=True)