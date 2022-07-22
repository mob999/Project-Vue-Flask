import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from urllib import response
from flask import *
from flask_cors import CORS
import main

UPLOAD_FOLDER = r'./demo/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
CORS(app)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.after_request
def after_request(response):
    '''
    Solve Cross Origin
    '''
    print('yes')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild'
    response.headers['X-Powered-By'] = '3.2.1'
    return response

def allowed_file(filename):
    '''
    Check if the file allowed
    '''
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def default():
    '''
    Default Route
    '''
    return redirect(url_for('static', filename='./index.html'))

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    '''
    Handle upload image request
    '''
    file = request.files['file']
    print("request for upload, filename is {file.filename}", datetime.datetime.now())
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        # shutil.copy(src_path, './demo/images')
        image_path = os.path.join('./demo/images', file.filename)
        # TODO FIX THE 'weight' PATH
        draw_path, s, res = main.run(img_path=image_path)
        return jsonify({
            'status':1,
            'origin_url': 'http://region-4.autodl.com:47238/demo/images/'+file.filename,
            'draw_url':    str(os.path.join('http://region-4.autodl.com:47238', draw_path)),
            'img_size': s,
            'result': res
        })

@app.route('/demo/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            img_data = open(f'./demo/{file}','rb').read()
            response = make_response(img_data)
            response.headers['Content-Type'] = 'image/jpg'
            return response

@app.route('/get-cur-model', methods=['GET', 'POST'])
def get_cur_model():
    f = open('./config.json', 'r')
    config = json.load(f)
    return jsonify(config)

@app.route('/get-models', methods=['GET', 'POST'])
def get_models():
    models = ''
    for model in os.listdir('./weights'):
        models += model + ' '
    response = make_response(models)
    return response

@app.route('/change-models', methods=['GET','POST'])
def change_models():
    print(request)
    model_type = request.args.get('type')
    model_name = request.args.get('name')
    print(model_type)
    print(model_name)
    config_json = open("./config.json", "r")
    config = json.load(config_json)
    if model_type == "yolo":
        config["det_weights"] = './weights/' + model_name
    elif model_type == "lprnet":
        config["rec_weights"] = './weights/' +  model_name
    config_json = open("./config.json", "w")
    print(config_json)
    json.dump(config, config_json)
    return jsonify(config)
            
        

if __name__ == '__main__':
    app.run(host='localhost', port=6006, debug=True)
