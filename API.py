#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:13:11 2018

@author: Ashwin
"""
from flask import Flask, request, jsonify
from API-Functions import preprocess
from common.configurator import Configurator
from common import appglobals

config = None
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/reduce', methods=['POST'])
def _reduce():
    try:
        content = request.get_json()
        return jsonify(reduce(content))
    except ValueError:
        return jsonify({'status' : False, 'message' : "Input needs to be in json format", "result": None})


if __name__ == '__main__':
    appglobals.config = Configurator('config.txt')
    app.run(debug = True, host='0.0.0.0', port=appglobals.config.getServerPort())
