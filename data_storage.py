'''
Descripttion: 
version: 39
Author: sikuai
Date: 2023-07-17 22:44:56
LastEditors: sikuai
LastEditTime: 2023-07-31 07:29:35
'''
# 调用数据库增删改查数据

import pymysql
import time

# 数据库连接
conn = pymysql.connect(host='192.168.1.66', user='bilibili',
                       password='304ab5ce4243ab9b', db='test')
cursor = conn.cursor()

def get_conn():
    global conn
    global cursor
    if conn is not None:
        try:
            conn.ping(True)
            return conn
        except Exception as e:
            print('发生异常:', e)
    try:
        conn = pymysql.Connect(host='192.168.1.6', user='bilibili', password='304ab5ce4243ab9b', db='test', port=3306, charset='utf8mb4', )
        return conn
    except Exception as e:
        print('发生异常:', e)


# # 创建表
# def create_table():
#   cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

# 查询uid数据

def select_data_uid(uid):
    get_conn()
    select_sql = "SELECT * FROM user_info WHERE uid = %s"
    cursor.execute(select_sql, [uid])
    result = cursor.fetchone()
    return (result)

# 查询投稿数据
def select_data_videos(uid):
    get_conn()
    select_sql = "SELECT * FROM user_post WHERE uid = %s"
    cursor.execute(select_sql, [uid])
    result = cursor.fetchone()
    return (result)

# 查询ip数据

def select_data_ip(ip):
    get_conn()
    print("IP为"+ip)
    select_sql = "SELECT * FROM black_ip_list WHERE ip = %s"
    cursor.execute(select_sql, [ip])
    result = cursor.fetchone()
    print("查询结果为"+str(result))
    return (result)

# 查询following数据

def select_data_following(uid):
    get_conn()
    select_sql = "SELECT * FROM user_following WHERE uid = %s"
    cursor.execute(select_sql, [uid])
    result = cursor.fetchone()
    return (result)

# 更新数据

def update_data(db, name, uid):
    update_sql = "UPDATE %s SET name = %s WHERE uid = %s"
    cursor.execute(update_sql, [name, uid])
    result = cursor.fetchone()
    return (result)

# 删除数据

def delete_data(db, uid):
    delete_sql = "DELETE FROM %s WHERE id = %s"
    cursor.execute(delete_sql, [uid])
    result = cursor.fetchone()
    return (result)

# 更新或插入用户主页数据

def replace_data_user(db, uid, name, sex, sign, full, timestamp):
    # 执行SQL
    sql = "REPLACE INTO "+str(db)+" (uid, name, sex, sign, full, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (uid, name, sex, sign, full, timestamp))  
        rowcount = cursor.rowcount
        conn.commit()
        cursor.close()
        return rowcount
        
    except Exception as e:
        print("插入数据异常:", e)
        conn.rollback()
        cursor.close()
        conn.close()
        
    # finally:
    #     conn.close()

# 更新或插入用户投稿数据
def replace_data_videos(db, uid, full, timestamp):
    # 执行SQL
    sql = "REPLACE INTO "+str(db)+" (uid, full, timestamp) VALUES (%s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (uid, full, timestamp))  
        rowcount = cursor.rowcount
        conn.commit()
        cursor.close()
        return rowcount
        
    except Exception as e:
        print("插入数据异常:", e)
        conn.rollback()
        cursor.close()
        conn.close()
        
    # finally:
    #     conn.close()

# 更新用户关注数据
def replace_data_following(uid,full,timestamp):
    # 执行SQL
    sql = "REPLACE INTO user_following (uid, full, timestamp) VALUES (%s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (uid, full, timestamp))  
        rowcount = cursor.rowcount
        conn.commit()
        cursor.close()
        return rowcount
        
    except Exception as e:
        print("插入数据异常:", e)
        conn.rollback()
        cursor.close()
        conn.close()
        
    # finally:
    #     conn.close()

# 更新或插入黑名单ip数据
def replace_data_ip(ip, url, ua, timestamp):
    # 执行SQL
    try:
        sql = "REPLACE INTO  black_ip_list (ip, url, ua, timestamp) VALUES (%s,%s,%s, %s)"
        cursor = conn.cursor()
        cursor.execute(sql, [ip,url, ua, timestamp])  
        rowcount = cursor.rowcount
        conn.commit()
        cursor.close()
        return rowcount
        
    except Exception as e:
        print("插入数据异常:", e)
        conn.rollback()
        cursor.close()
        conn.close()
        
# 手动调用测试
if __name__ == '__main__':
    uid = "1234323"
    name = "1234323"
    sex = "1"
    full = "{'face':'123'}"
    sign = "1234323"
    db = "user_info"
    timestamp = str(time.time()).split(".")[0]
    replace_data_user(db, uid, name, sex, sign, full, timestamp)
    # # 提交并关闭
    # conn.commit()
    # cursor.close()
    # conn.close()

