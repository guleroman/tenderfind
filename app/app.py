import logging
import requests
import os

from flask import Flask, jsonify, request, json, make_response
from search import get_similar_tovar, get_similar_tovar_v2, get_similar_tovar_v3
import yaml
from flask_cors import CORS, cross_origin

config_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'config.yml'))
config = yaml.load(open(config_path))

app = Flask(__name__)
app.config.update(config)
logger = logging.getLogger(__name__)
CORS(app)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler(app.config['LOGFILE'])
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

def set_logger(logger):
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
logger = set_logger(logger)


@app.route('/api/v1/themes/',methods=['POST'])
@cross_origin(origins="*", methods=['POST','OPTIONS'], allow_headers="*")
def task_processing_themes_processing():
    try:
        req = json.loads(request.data)
        get_text = req['text']
    except:
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    try:
        class_p = req['class_p']
    except:
        class_p = None
    
    try:
        class_t = req['class_t']
    except:
        class_t = None
    
    result = get_similar_tovar(class_p=class_p, class_t=class_t, text = get_text)
    resp = make_response(jsonify({"result":result}))
    return resp

@app.route('/api/v2/themes/',methods=['POST'])
@cross_origin(origins="*", methods=['POST','OPTIONS'], allow_headers="*")
def task_processing_themes_processing_v2():
    try:
        req = json.loads(request.data)
        get_text = req['text']
        try:
            class_p = req['class_p']
        except:
            class_p = None

        try:
            class_t = req['class_t']
        except:
            class_t = None

        result = get_similar_tovar_v2(class_p=class_p, class_t=class_t, text = get_text)
        resp = make_response(jsonify({"result":result})) 
        #resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        #try:
        get_text = None
        get_texts = req['texts']
        result = get_similar_tovar_v3(texts = get_texts)
        resp = make_response(jsonify({"result":result}))
        return resp
        #except:
         #   return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)