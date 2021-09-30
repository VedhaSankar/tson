#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import *
from core import convert_json_to_tson, convert_tson_to_json
from werkzeug.utils import secure_filename
import json
import glob
import os

app = Flask(__name__)


UPLOAD_PATH = "static/uploads/"
app.config["UPLOAD_FOLDER"] = UPLOAD_PATH


'''
    http://127.0.0.1:4000/
'''
@app.route('/', methods=['GET'])
def home():
 
    return render_template('demo.html')

@app.route('/', methods = ['GET', 'POST'])
def upload_files():

    if request.method == 'POST':

        f = request.files['file']

        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename)

        update_json(filename)

    return render_template('demo.html')

'''
    http://127.0.0.1:4000/to/tson
'''
@app.route('/to/tson', methods = ['GET'])
def convert_to_tson():

    file_name = get_latest_file_name()

    path_to_json = f'{UPLOAD_PATH}{file_name}'

    data = get_json(path_to_json)

    res, tson = convert_json_to_tson(data)

    save_json(tson)

    return tson

def get_json(file_name):

    json_file = open(file_name)
    json_data = json.load(json_file)

    return json_data

def save_json(data):

    with open('static/downloads/data.json', 'w') as f:
        json.dump(data, f)

def update_json(file_name):

    data = {
        "file_name" : file_name
    }

    with open('static/temp.json', 'w') as f:
        json.dump(data, f)

def get_latest_file_name():

    json_file = open('static/temp.json')
    json_data = json.load(json_file)

    file_name = json_data['file_name']

    return file_name

if __name__ == '__main__':

    app.run('0.0.0.0', 4000, True)
