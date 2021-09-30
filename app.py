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


# @app.route('/', methods=['POST'])
# def upload_files():

#     uploaded_file = request.files['file']

#     filename = secure_filename(uploaded_file.filename)

#     if filename != '':

#         file_ext = os.path.splitext(filename)[1]

#         uploaded_file.save(os.path.join('static/uploads', filename))


#     return '', 204




@app.route('/', methods = ['GET', 'POST'])
def upload_files():

    if request.method == 'POST':
        f = request.files['file']

        # global filename

        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename)

    return render_template('demo.html')


'''
    http://127.0.0.1:4000/to/tson
'''
@app.route('/to/tson', methods=['GET'])
def convert_to_tson():

    list_of_files = glob.glob('static/uploads/*.json') # * means all if need specific format then *.csv
    filename = max(list_of_files, key = os.path.getctime)
        
    path_to_json = f'{filename}'

    data = get_json(path_to_json)


    res, tson = convert_json_to_tson(data)

    save_json(tson)

    # return send_file(save_json(tson), as_attachment = True, attachment_filename='data.json')

    return send_file("static/downloads/data.json", as_attachment = True)
    # return "success"


def get_json(file_name):

    json_file = open(file_name)
    # print (json_file)
    # decoded_data=codecs.decode(json_file, 'utf-8-sig')
    json_data = json.load(json_file)

    return json_data


def save_json(data):

    with open('static/downloads/data.json', 'w') as f:
        json.dump(data, f)



if __name__ == '__main__':
    #app.debug = True;1
    app.run('127.0.0.1', 4000, True)
