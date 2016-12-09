#codeing:utf-8
#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("127.0.0.1","root","root","2015",charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute('select * from go_brand ')

# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
#
# print ("Database version : %s " % data)


# 获取所有记录列表
results = cursor.fetchall()
for row in results:
    fname = row[3]
    print ("Database version : %s " % fname)
# 关闭数据库连接
db.close()