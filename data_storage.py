'''
Descripttion: 
version: 39
Author: sikuai
Date: 2023-07-17 22:44:56
LastEditors: sikuai
LastEditTime: 2023-07-21 09:13:10
'''
# 调用数据库增删改查数据

import pymysql
import time

# 数据库连接
conn = pymysql.connect(host='192.168.1.6', user='bilibili',
                       password='304ab5ce4243ab9b', db='test')
cursor = conn.cursor()

# # 创建表
# def create_table():
#   cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

# 插入数据


def insert_data(db, name):
    insert_sql = "INSERT INTO %s (name) VALUES (%s)"
    cursor.execute(insert_sql, [name])
    result = cursor.fetchone()
    return (result)

# 查询数据


def select_data(db, uid):
    select_sql = "SELECT * FROM %s WHERE uid = %s"
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

# 更新或插入用户主页数据
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
        
    finally:
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

