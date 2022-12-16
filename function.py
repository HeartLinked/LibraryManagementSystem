import pymysql.cursors
from pymysql.constants import CLIENT
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)

connection = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', \
    password = 'LFYmemories0907', db = 'Library', charset = 'utf8mb4', \
         cursorclass = pymysql.cursors.DictCursor,  client_flag = CLIENT.MULTI_STATEMENTS)

try:
    cursor = connection.cursor()
    sql = "select * from card"
    cursor.execute(sql)
    result2 = cursor.fetchall()
    #for data in result2:
     #   print(data)
except Exception :print("Query Error!")
connection.commit()
cursor.close()
connection.close()

def check(username, password, mode) :
    #return True
    print(type(username), type(password))
    print(username, password)
    for data in result2:
        str_ID = str(data['card_ID'])
        if(str_ID == username and data['card_password'] == password and data['card_authority'] == mode) :
            return True
    else:
        return False
