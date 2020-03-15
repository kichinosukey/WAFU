import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from flask import Blueprint, request, jsonify

from sample.config import PREFIX_API, URL_INDEX_API


api = Blueprint(PREFIX_API, __name__)


@api.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return jsonify({'message': 'hello', 'method': request.method})
    
    elif request.method == 'POST':
        return jsonify({'message': 'hello', 'method': request.method})