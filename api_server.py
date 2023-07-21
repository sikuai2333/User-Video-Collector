'''
Descripttion: 
version: 39
Author: sikuai
Date: 2023-07-17 22:44:34
LastEditors: sikuai
LastEditTime: 2023-07-19 16:29:03
'''
# 接收请求

# import data_collector

from flask import Flask
from flask import render_template, jsonify, request, redirect, make_response
from flask_cors import CORS
import os
import json
import time
import requests
import base64
import re
import redis

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/api/<name>')
def api(name):
    data = str(name)
    status = check_data(data)
    return status

#user主页采集，传入UID作为参数
@app.route('/collect_user') 
def collect_user():
    # 获取uid参数
    uid = request.values.get('uid')
    # 参数校验
    if not uid:
        return jsonify({'code': 500, 'message': '未接受到uid'})
    # 提取uid中的数字
    match = re.search(r'\d+', uid)
    if not match:
        return jsonify({'code': 500, 'message': 'uid非数字'})
    uid = str(match.group())
    # 范围校验
    if 5 < len(uid) < 30:
        # 参数验证成功,构造任务数据
        task = {'uid': uid, 'type': 'user'} 
        # 写入采集队列（此处是rpush，lpop右存左取）
        redis_client.rpush('collect_tasks', task)
        # 返回结果
        return jsonify({'code': 200, 'message': '用户主页采集任务已提交'})
    return jsonify({'code': 400, 'message': 'uid长度错误'})

#用户投稿采集
@app.route('/collect_videos') 
def collect_videos():
    # 获取uid参数
    uid = request.values.get('uid')
    # 参数校验
    if not uid:
        return jsonify({'code': 500, 'message': '未接受到uid'})
    # 提取uid中的数字
    match = re.search(r'\d+', uid)
    if not match:
        return jsonify({'code': 500, 'message': 'uid非数字'})
    uid = str(match.group())
    # 范围校验
    if 5 < len(uid) < 30:
        # 参数验证成功,构造任务数据
        task = {'uid': uid, 'type': 'videos'} 
        # 写入采集队列（此处是rpush，lpop右存左取）
        redis_client.rpush('collect_tasks', task)
        # 返回结果
        return jsonify({'code': 200, 'message': '用户主页采集任务已提交'})
    return jsonify({'code': 400, 'message': 'uid长度错误'})


def check_data(data):
  sql_injection_pattern = r'(.*)(|and|like|exec|insert|select|drop|grant|alter|delete|update|count|chr|mid|master|truncate|char|delclare|or|;)(.*)'
  if re.search(sql_injection_pattern, data, re.IGNORECASE):
    return (str("请输入规范的参数!"), 400)
  else:
    return (str("参数正常"), 200)


if __name__ == '__main__':
    # 创建Redis连接
    redis_client = redis.Redis(host='192.168.1.6', port=6379)
    # flask启动
    app.run(debug=True, port=5000)
