import logging
import requests
import os

from flask import Flask, jsonify, request, json, make_response
from search import get_similar_tovar
import yaml


config_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'config.yml'))
config = yaml.load(open(config_path))
app = Flask(__name__)
app.config.update(config)
logger = logging.getLogger(__name__)

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
def task_processing_themes_processing():
    try:
        req = json.loads(request.data)
    except:
        return make_response(jsonify({"_status_code":422,"error":{"info":"incorrect POST-request"}}),422)

    result = get_similar_tovar(req['text'])
    resp = make_response(jsonify({"result":result})) 
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

    # if processing_result['_status_code'] != 200: 
    #     return make_response(jsonify(processing_result['error']), processing_result['_status_code'])
    # elif processing_result['_status_code'] == 200:
    #     resp = make_response(jsonify({"result":processing_result["themes"]})) 
    #     resp.headers['Access-Control-Allow-Origin'] = '*'
    #     return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)