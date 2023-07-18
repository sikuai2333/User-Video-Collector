'''
Descripttion: 
version: 39
Author: sikuai
Date: 2023-07-17 22:44:34
LastEditors: sikuai
LastEditTime: 2023-07-18 17:10:24
'''
# 接收请求

import data_collector

from flask import Flask
from flask import render_template, jsonify, request, redirect, make_response
from flask_cors import CORS
import os
import json
import time
import requests
import base64
import re

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/api/<name>')
def api(name):
    data = str(name)
    status = check_data(data)
    return status



def check_data(data):
  sql_injection_pattern = r'(.*)(|and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or|;)(.*)'
  if re.search(sql_injection_pattern, data, re.IGNORECASE):
    return (str("请输入规范的参数!"), 400)
  else:
    return (str("参数正常"), 200)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
