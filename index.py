import os
import sys
sys.path.append(os.path.join(os.path.dirname(__name__), './'))
import argparse

from flask import Flask

from apps.config import FILE_NAME_URL_PREFIX, ROOTDIR, URL_INDEX_AUTH

app = Flask(__name__)

# register app
from apps.auth import auth
app.register_blueprint(auth, url_prefix=URL_INDEX_AUTH)

from apps.sample.view import sample, URL_INDEX_VIEW
app.register_blueprint(sample, url_prefix=URL_INDEX_VIEW)

from apps.sample.body import api, URL_INDEX_API
app.register_blueprint(api, url_prefix=URL_INDEX_API)

# set secret key
app.secret_key = 'test key'

def set_parser():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-ip", "--ip_addr", type=str, default="127.0.0.1", help="host IP address")
    parser.add_argument("-p", "--port", type=int, default=5000, help="port number")
    parser.add_argument("-a", "--api_addr", type=str, default="127.0.0.1", help="API address")
    parser.add_argument("-apps", "--apps", nargs="*")
    parser.add_argument("--debug", action="store_true", help="turn on debug mode")

    return parser.parse_args()

if __name__ == '__main__':

    args = set_parser()

    port = args.port
    ip = args.ip_addr
    api_addr = args.api_addr
    debug = args.debug
    if args.apps is None:
        app_name_list = ['sample']
    else:
        app_name_list = args.apps

    # write out config file
    url_prefix = 'http://' + api_addr + ':' + str(port)

    for app_name in app_name_list:
        filename = ROOTDIR + app_name + '/' + FILE_NAME_URL_PREFIX
        with open(filename, mode="w") as f:
            f.write(url_prefix)

    app.run(host=ip, port=port, debug=args.debug, threaded=True)