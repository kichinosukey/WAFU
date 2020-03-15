from datetime import datetime

from flask import session


def clear_flash(session_key_flash):
    session.pop(session_key_flash, None)

def get_datetimenow(style='%Y-%m-%d_%H%M%S'):
    return datetime.now().strftime(style) 

def is_allowed_file(filename, allowed_file_ext=['xlsx']):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_file_ext