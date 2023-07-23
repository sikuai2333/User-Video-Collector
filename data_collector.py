'''
Descripttion: 
version: 39
Author: sikuai
Date: 2023-07-17 22:44:43
LastEditors: sikuai
LastEditTime: 2023-07-23 14:49:00
'''
# 请求API采集数据

import data_storage
import get_wbi
import redis
import time
import requests
import json

redis_client = redis.Redis(host='192.168.1.6', port=6379)
# 用户主页数据
def collect_user_data(uid):
    print("用户主页采集任务，UID="+str(uid))
    time.sleep(10)
    try:
        url = "https://api.bilibili.com/x/space/wbi/acc/info?"
        wbi = get_wbi.start(params={'mid': str(uid)})
        print("获取到签名"+str(wbi))
        mid = str(uid)
        wts = str(wbi).split("&")[1].replace("wts=","")
        w_rid = str(wbi).split("&")[2].replace("w_rid=","")
        url_full = url+"mid="+str(mid)+"&wts="+str(wts)+"&w_rid="+str(w_rid)
        print(url_full)
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/112.0.0.0 Edg/112.048',
        'Accept': '*/*',
        'Host': 'api.bilibili.com',
        'Connection': 'keep-alive'
        }
        res = requests.get(url=url_full,headers=headers,verify=False).text
        # print(res)
        # with open("collect_user_data.txt","w",encoding="utf-8")as f:
        #     f.write(res)
        #解析json存入数据库，此处直接解析可能会有问题，如果接口因频率过快会取不到key直接报错
        code = json.loads(res)["code"]
        if code == int(-403):
            print("用户主页采集接口错误")
            return("用户主页采集接口错误")
        else:
            print(res)
            data = json.loads(res)["data"]
            # 直接存入整个json，前端展示再解析
            db = "user_info"
            name = str(data["name"])
            uid = str(data["mid"])
            sex = str(data["sex"])
            sign = str(data["sign"])
            timestamp = str(str(time.time()).split(".")[0])
            full = str(res)
            result = data_storage.replace_data_user(db, uid, name, sex, sign, full, timestamp)
            print("成功影响行数："+str(result))
            return("用户主页采集成功")
    except Exception as e:
        # 捕获到异常后,打印异常信息
        print('发生异常:', e)
# 用户投稿数据
def collect_user_videos(uid):
    print("用户投稿采集任务，UID="+str(uid))
    time.sleep(10)
    try:
        url = "https://api.bilibili.com/x/space/wbi/arc/search?"
        wbi = get_wbi.start(params={'mid': str(uid),'pn':'1','ps':'50'})
        print("获取到签名"+str(wbi))
        mid = str(uid)
        wts = str(wbi).split("&")[3].replace("wts=","")
        w_rid = str(wbi).split("&")[4].replace("w_rid=","")
        url_full = url+"mid="+str(mid)+"&pn=1&ps=50"+"&wts="+str(wts)+"&w_rid="+str(w_rid)
        print(url_full)
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
        'Host': 'api.bilibili.com',
        'Connection': 'keep-alive',
        'Cookie':'',
        'Refer':'https://space.bilibili.com/1871207387/video',
        'Accept':'application/json, text/plain, */*'
        }
        res = requests.get(url=url_full,headers=headers,verify=False).text
        # print(res)
        # with open("collect_user_data.txt","w",encoding="utf-8")as f:
        #     f.write(res)
        #解析json存入数据库，此处直接解析可能会有问题，如果接口因频率过快会取不到key直接报错
        code = json.loads(res)["code"]
        if code == int(-403):
            print("用户投稿采集接口错误")
            return("用户投稿采集接口错误")
        elif code == int(-799):
            print("接口频繁")
            print(res)
            return("接口频繁")
        else:
            # print(res)
            # 直接存入整个json，前端展示再解析
            db = "user_post"
            # with open("collect_user_data.txt","w",encoding="utf-8")as f:
            #     f.write(res)
            timestamp = str(str(time.time()).split(".")[0])
            full = str(res)
            result = data_storage.replace_data_videos(db, uid, full, timestamp)
            print("成功影响行数："+str(result))
            return("用户投稿采集成功")
    except Exception as e:
        # 捕获到异常后,打印异常信息
        print('发生异常:', e)
# 用户关注列表
def collect_user_follows(uid,sessdata):
    print("用户关注采集任务，UID="+str(uid),"sessdata值为"+str(sessdata))
    # time.sleep(10)
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
        'Host': 'api.bilibili.com',
        'Connection': 'keep-alive',
        'Cookie':'SESSDATA='+str(sessdata),
        'Refer':'https://space.bilibili.com/1871207387/video',
        'Accept':'application/json, text/plain, */*'
        }
        pn = 1
        url = "https://api.bilibili.com/x/relation/followings?vmid="+str(uid)+"&pn="+str(pn)+"&ps=50"
        print(url)
        res = requests.get(url=url,headers=headers).json()
        #解析json存入数据库，此处直接解析可能会有问题，如果接口因频率过快会取不到key直接报错
        code = res["code"]
        first_list = res["data"]["list"][0]
        if code == int(0):
            total = res["data"]["total"]
            page = (total//50)+1
            print("总页数:"+str(page))
            full_list = []
            full_list.append(first_list)
            for pn in range(2,page+1):
                url = "https://api.bilibili.com/x/relation/followings?vmid="+str(uid)+"&pn="+str(pn)+"&ps=50"
                res = requests.get(url=url,headers=headers).json()
                print(pn)
                # time.sleep(3)
                lists = res["data"]["list"]
                for list in lists:
                    full_list.append(list)
            # 拼接list然后存入
            timestamp = str(str(time.time()).split(".")[0])
            full = json.dumps(full_list)
            result = data_storage.replace_data_follows(uid, full, timestamp)
            print("成功影响行数："+str(result))
            return("用户投稿采集成功")

    except Exception as e:
        # 捕获到异常后,打印异常信息
        print('发生异常:', e)
    
while True:
    # 获取任务队列（此处是rpush，lpop右存左取）
    task = redis_client.lpop('collect_tasks')
    if task:
        # bytes转str
        task_str = task.decode('utf-8')  
        # str转字典
        task = eval(task_str)
        # 解析任务
        type = task['type']
        # 采集用户主页
        if type == 'user':
            uid = task['uid']
            # 执行用户数据采集
            result = collect_user_data(uid)
        # 采集用户投稿
        if type == 'videos':
            uid = task['uid']
            result = collect_user_videos(uid)        
        # 采集用户关注
        if type == 'follows':
            sessdata = task['sessdata']
            uid = task['uid']
            result = collect_user_follows(uid,sessdata)
        # 将结果写入结果队列  -任务提交到采集队列后,会异步地被采集函数消费。如果直接return,则会同步等待采集完成,效率低。
        redis_client.lpush('collect_results', result)
    else:
        # 队列空时短暂睡眠
        time.sleep(10)