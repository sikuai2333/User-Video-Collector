'''
Descripttion: 
version: 39
Author: sikuai
Date: 2023-07-17 22:44:34
LastEditors: sikuai
LastEditTime: 2023-07-31 07:53:23
'''
# 接收请求

# import data_collector
import data_storage

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
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

@app.route('/api/<name>')
def api(name):
    data = str(name)
    # request.remote_addr 客户端 IP 地址
    # request.method 请求使用的 HTTP 方法(GET、POST等) 
    # request.url 请求的完整 URL 地址
    # request.args GET 请求的 URL 参数字典
    # request.form POST 请求的表单参数字典
    # request.cookies 请求的 Cookie 字典
    # request.headers 请求的 Header 字典
    cookie =  request.cookies
    headers = request.headers.get("User-Agent")
    json_data_ua = {"User-Agent":headers}
    full_url = request.url
    # 记录ip
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    status = check_data(headers,data)
    result = black_ip_list(ip)
    if status and result == None:
        print(headers)
        # return jsonify(json_data_ua)
        return jsonify({'code': 200, 'message': 'success'})
    else:
        return jsonify({'code': 444, 'message': '封禁时间戳'+result[1]})

#user主页-采集，传入UID作为参数
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

#用户投稿-采集
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
        return jsonify({'code': 200, 'message': '用户投稿采集任务已提交'})
    return jsonify({'code': 400, 'message': 'uid长度错误'})

#用户关注-采集
@app.route('/collect_following') 
def collect_following():
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
    if 5 < len(uid) < 30 :
        # 参数验证成功,构造任务数据
        task = {'uid': uid, 'type': 'following'} 
        # 写入采集队列（此处是rpush，lpop右存左取）
        redis_client.rpush('collect_tasks', task)
        # 返回结果
        return jsonify({'code': 200, 'message': '用户关注采集任务已提交'})
    return jsonify({'code': 400, 'message': 'uid长度错误或sessdata为空'})

#user主页-搜索，传入UID作为参数
@app.route('/search_user') 
def search_user():
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
        result = data_storage.select_data_uid(uid)
        print(result)
        if result == None:
            return jsonify({'code': 503, 'message': '查询不到信息'})
        else:
            # 返回结果
            return jsonify({'code': 200, 'message': result[4]})
    return jsonify({'code': 400, 'message': 'uid长度错误'})

# user投稿-搜索，传入UID作为参数
@app.route('/search_videos')
def search_videos():
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
        result = data_storage.select_data_videos(uid)
        print(result)
        if result == None:
            return jsonify({'code': 503, 'message': '查询不到信息'})
        else:
            # 返回结果
            return jsonify({'code': 200, 'message': result[1]})
#user关注列表-搜索，传入UID作为参数
@app.route('/search_follows') 
def search_following():
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
        result = data_storage.select_data_following(uid)
        print(result)
        if result == None:
            return jsonify({'code': 503, 'message': '查询不到信息'})
        else:
            # 返回结果
            return jsonify({'code': 200, 'message': result[1]})
    return jsonify({'code': 400, 'message': 'uid长度错误'})
# 存储IP黑名单
def ban_ip(ip,ua,url):
    print(ip)
    print(ua)
    print(url)
    timestamp = str(str(time.time()).split(".")[0])
    data_storage.replace_data_ip(ip,url,ua,timestamp)
# 获取IP黑名单
def black_ip_list(ip):
    result = data_storage.select_data_ip(ip)
    print(result)
    return(result)

def check_data(headers,data):
    sql_injection_pattern = re.compile(r'([(;)]+\s*(or|and))|(=|>|<|>=|<=|\*|like)|(select|insert|update|delete|drop|exec|count|chr|mid|master|truncate|char|declare|or|base64_decode|information_schema|hack|shell|spy|phpspy|eval|mysql_history|bash_history|DS_Store|idea|user\.ini|bak|inc|old|mdb|sql|php~|swp|java|class|iframe|script|body|img|layer|div|meta|style|base|object|input|connection_id|;)', re.IGNORECASE)
    ua_pattern = re.compile(r'(\s*(sqlmap|havij|zmeu|BabyKrokodil|netsparker|hydra|libwww|BBBike|Parser|Nikto|w3af|owasp|fimap|pangolin|dirbuster|censys|fofa|zoomeye|audit|nmap|HTTrack))', re.IGNORECASE)
    if sql_injection_pattern.search(data) or ua_pattern.search(headers):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        ban_ip(ip=ip,url=request.url,ua=request.headers.get("User-Agent"))
        # 是危险函数
        return False
    else:
        # 不是危险函数
        return True


if __name__ == '__main__':
    # 创建Redis连接
    redis_client = redis.Redis(host='192.168.1.66', port=6379)
    # flask启动
    app.run(debug=True, port=5000, host="0.0.0.0")
