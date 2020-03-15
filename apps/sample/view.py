import os
import sys
sys.path.append(os.path.join(os.path.dirname(__name__), '../'))
from datetime import datetime

import requests
from flask import Blueprint, render_template, request, session, jsonify, g
from flask import redirect, flash, send_file
from werkzeug.utils import secure_filename

from apps.config import (
    FILE_NAME_URL_PREFIX, SESSION_KEY_USERID, 
    SESSION_KEY_USERNAME, SESSION_KEY_PASSWORD, SESSION_KEY_URL_INDEX, 
    SESSION_KEY_URL_PREFIX, ROOTDIR, URL_INDEX_AUTH)
from apps.sample.config import (
    ALLOWED_EXTENSIONS, APP_DIR, CSV_MIMETYPE,
    FORM_KEY_DL_FILEPATH, FORM_KEY_UPLOAD_DATADIR, FORM_KEY_UPLOAD_FILES,
    SESSION_KEY_DATADIR, SESSION_KEY_FLASH, UPLOAD_DIR, URL_INDEX_API, 
    URL_INDEX_VIEW, VIEW_PREFIX)


sample = Blueprint('sample', __name__, template_folder='./templates', static_folder='./static')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_flash():
    session.pop(SESSION_KEY_FLASH, None)

def get_datetimenow(style='%Y-%m-%d_%H%M%S'):
    return datetime.now().strftime(style) 

@sample.before_app_first_request
def load_url_prefix():
    filename = ROOTDIR + VIEW_PREFIX + '/' + FILE_NAME_URL_PREFIX
    with open(filename, mode="r") as f:
        session[SESSION_KEY_URL_PREFIX] = f.read()
    f.close()

    session[SESSION_KEY_URL_INDEX] = URL_INDEX_VIEW

@sample.before_request
def before_request():
    clear_flash()

    if session.get(SESSION_KEY_USERNAME):
        username = session[SESSION_KEY_USERNAME]
        status = 'User Name: %s ' % username
        print('*'*5, username, '*'*5)
        flash(status)
        if session.get(SESSION_KEY_DATADIR):
            datadir = session[SESSION_KEY_DATADIR]
            status = 'Set directory: %s' % datadir
            flash(status)
    else:
        return redirect(URL_INDEX_AUTH + '/login')

@sample.after_request
def after_request(response):
    g.db.close_db()
    return response

@sample.route('/')
def index():
    return render_template('sample/index.html')

@sample.route('/hello')
def hello():
    
    r = requests.get(session[SESSION_KEY_URL_PREFIX] + URL_INDEX_API + '/hello')

    res = r.json()

    return res

@sample.route('/demo')
def bokeh_demo():
    return render_template('sample/demo.html')

@sample.route('/download', methods=['GET'])
def download():

    if request.method == 'GET':
        return render_template('sample/download.html')

@sample.route('/download/file', methods=['GET'])
def download_file():

    if request.method == 'GET':
        
        filename = request.args.get(FORM_KEY_DL_FILEPATH)
        if filename is None:
            return redirect(URL_INDEX_VIEW)

        return send_file(filename, attachment_filename=filename, as_attachment=True, mimetype=CSV_MIMETYPE)

@sample.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if not session.get(SESSION_KEY_DATADIR):
            upload_dir = ROOTDIR + APP_DIR + UPLOAD_DIR
            datadir = upload_dir + get_datetimenow() + '/'
        else:
            datadir = session[SESSION_KEY_DATADIR]

        if FORM_KEY_UPLOAD_FILES not in request.files:
            flash('No file part')
            return redirect(URL_INDEX_VIEW)

        files = request.files.getlist(FORM_KEY_UPLOAD_FILES)
        for file in files:
            if file.filename == '':
                flash('No selected file') 
                return redirect(URL_INDEX_VIEW)

            if not allowed_file(file.filename):
                flash('File ext is not valid')
                return redirect(URL_INDEX_VIEW + '/upload')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(datadir, filename))

        flash('File upload has successed.')
        return redirect(URL_INDEX_VIEW)
    
    elif request.method == 'GET':

        datadir = request.args.get(FORM_KEY_UPLOAD_DATADIR)
        
        if datadir:
            upload_dir = ROOTDIR + APP_DIR + UPLOAD_DIR
            if not os.path.exists(upload_dir):
                os.mkdir(upload_dir)

            datadir = upload_dir + datadir
            if not os.path.exists(datadir):
                os.mkdir(datadir)
                session[SESSION_KEY_DATADIR] = os.path.join(datadir, '') 
                status = 'The directory(%s) was created successfuly.' % datadir
            else:
                status = 'The dirname(%s) already exists.'
            flash(status)

        return render_template('sample/upload.html')