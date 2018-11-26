#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:13:11 2018

@author: Trudeau R. Fernandes
"""
from flask import Flask, request, jsonify
from preprocess.preprocess import preprocess
from common.configurator import Configurator
from postprocess import BusinessCloud
from common import appglobals

config = None
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/preprocess', methods=['POST'])
def _preprocess():
    try:
        content = request.get_json()
        return jsonify(preprocess(content))
    except ValueError:
        return jsonify({'status' : False, 'message' : "Input needs to be in json format", "result": None})


if __name__ == '__main__':
    appglobals.config = Configurator('config.txt')
    BusinessCloud.ServiceManagement.registerEndPoints(app)
    BusinessCloud.ITHelpDesk.registerEndPoints(app)
    BusinessCloud.WarrantyAndClaims.registerEndPoints(app)
    app.run(debug = True, host='0.0.0.0', port=appglobals.config.getServerPort())
