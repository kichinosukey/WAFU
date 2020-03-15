import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import binascii
import hashlib

from flask import Blueprint, request, jsonify, g, redirect, render_template, flash, session

from apps.db import User, TABLE_NAME_USER, TABLE_DEFINITION_USER, USER_TABLE_IDX, COL_IDX, COL_USER_NAME, COL_USER_PASSDIGEST
from apps.config import (APP_NAME_AUTH, DBNAME_AUTH, DBDIR_AUTH, 
                FORM_KEY_PASSWORD, FORM_KEY_USERID, FORM_KEY_USERNAME,
                SESSION_KEY_URL_INDEX, SESSION_KEY_PASSWORD, SESSION_KEY_USERID, 
                SESSION_KEY_USERNAME, URL_INDEX_AUTH)


auth = Blueprint(APP_NAME_AUTH, __name__, template_folder='./templates', static_folder='./static')


def convert_str2digest(data):
    """Convert byte string to digest
    
    Args:
        data (str):
    """
    string = binascii.b2a_hex(bytes(data.encode()))
    str_digest = hashlib.sha1(string).digest()
    return binascii.b2a_hex(str_digest).decode()

def check_password_hash(left, right):
    """Check the digest from input data
    
    Args:
        left(str): The correct digest string
        right(str): The string to be checked its digest 
    """
    return left == convert_str2digest(right)

def init_db():
    return User(DBDIR_AUTH + DBNAME_AUTH)

@auth.before_request
def before_request():
    g.db = init_db()

@auth.after_request
def after_request(response):
    g.db.close_db()
    return response

@auth.before_app_request
def load_logged_in():
    user_id = session.get(SESSION_KEY_USERID)
    g.db = init_db()

    if user_id is None:
        g.user = None
    else:
        query = 'SELECT * FROM ' + TABLE_NAME_USER + ' WHERE id = ?'
        g.user = g.db.exec_sql_fetchone(query, (user_id, ))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        username = request.form.get(FORM_KEY_USERNAME)
        password = request.form.get(FORM_KEY_PASSWORD)

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif g.db.exec_sql_fetchone('SELECT id FROM user WHERE username = ?', (username, )) is not None:
            error = 'User %s already exists.' % username

        if error is None:
            query = 'INSERT INTO user (' + COL_USER_NAME + ',' + COL_USER_PASSDIGEST + ') VALUES (?, ?)'
            g.db.exec_sql(query, (username, convert_str2digest(password)))
            g.db.commit_db()

            return redirect('login')

        flash(error)

    return render_template(APP_NAME_AUTH + '/signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get(FORM_KEY_USERNAME)
        password = request.form.get(FORM_KEY_PASSWORD)
        user = g.db.exec_sql_fetchone('SELECT * FROM user WHERE username = ?', (username, ))

        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[USER_TABLE_IDX[COL_USER_PASSDIGEST]], password):
            error = 'Incorrect password.'
        
        if error is None:
            # session.clear() #FIXME
            session[SESSION_KEY_USERID] = user[USER_TABLE_IDX[COL_IDX]]
            session[SESSION_KEY_USERNAME] = user[USER_TABLE_IDX[COL_USER_NAME]]
            return redirect(session[SESSION_KEY_URL_INDEX])

        flash(error)
    
    return render_template(APP_NAME_AUTH + '/login.html')

@auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(URL_INDEX_AUTH + '/login')