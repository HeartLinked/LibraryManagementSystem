import pymysql.cursors
from pymysql.constants import CLIENT
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math
import function

app = Flask(__name__)

connection = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', \
    password = 'LFYmemories0907', db = 'Library', charset = 'utf8mb4', \
         cursorclass = pymysql.cursors.DictCursor,  client_flag = CLIENT.MULTI_STATEMENTS)

try:
    cursor = connection.cursor()
    sql = "select * from books"
    cursor.execute(sql)
    result = cursor.fetchall()
    for data in result :
        print (data)
except Exception :print("Query Error!")
connection.commit()

username = password = ""
count = 0

@app.route('/')
def hello_world():  # put application's code here
    # return index html
    return render_template('index.html')

@app.route('/login', methods = ["POST"])
def hello_login():  # put application's code here
    # return index html
    # request.form.get()
    global username
    global password
    username = request.form.get('username')
    password = request.form.get('password')
    mode = request.form.get('mode')
    if function.check(username, password, mode) == True:
        if (mode == 'root'):
            return render_template('admin.html', data_list=result)
        else:
            sql = "select card_br_now from card where card_ID = " + username
            cursor.execute(sql)
            K = cursor.fetchall()
            for data in K:
                k = int(data['card_br_now'])
            connection.commit()
            sql = "select card_br_tot from card where card_ID = " + username
            cursor.execute(sql)
            M = cursor.fetchall()
            for data in M:
                m = int(data['card_br_tot'])
            connection.commit()
            return render_template('student.html', data_list=result, k = k, m = m)
    else:
        return render_template('index.html')

@app.route('/delete/<ID>')
def delele_book(ID):
    global result
    for data in result :
        str_ID = str(data['book_ID'])
        if str_ID == ID:
            sql = "delete from books where book_ID = " + ID
            cursor.execute(sql)
            connection.commit()
            break

    sql = "select * from books"
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    return render_template('admin.html', data_list = result)

@app.route('/delete_student/<ID>')
def delele_student(ID):

    sql = "delete from card where card_ID = " + ID
    cursor.execute(sql)
    connection.commit()

    sql = "select card_ID, card_password, card_br_tot, card_br_now from card where card_authority = 'student'"
    cursor.execute(sql)
    query_user = cursor.fetchall()
    connection.commit()

    return render_template('query_user.html', data_list=query_user)

@app.route('/borrow/<ID>')
def borrow_book(ID):
    global result
    global count
    count += 1
    for data in result :
        str_ID = str(data['book_ID'])
        if str_ID == ID:
            sql = "update books set book_inv_number = book_inv_number - 1 where book_ID = " + ID
            cursor.execute(sql)
            connection.commit()
            sql = "update card set card_br_now = card_br_now + 1 where card_ID = " + username
            cursor.execute(sql)
            connection.commit()
            now_date = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            sql = "insert into borrow values(" + str(count) + "," + username + ", " + ID + ",'" + now_date + "',0)"
            cursor.execute(sql)
            connection.commit()
            break

    sql = "select * from books"
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()

    sql = "select card_br_now from card where card_ID = " + username
    cursor.execute(sql)
    K = cursor.fetchall()
    for data in K:
        k = int(data['card_br_now'])
    connection.commit()
    sql = "select card_br_tot from card where card_ID = " + username
    cursor.execute(sql)
    M = cursor.fetchall()
    for data in M:
        m = int(data['card_br_tot'])
    connection.commit()
    return render_template('student.html', data_list=result, k=k, m=m)

@app.route('/revert/<ID>')
def revert_book(ID):
    global result

    sql = "update books set book_inv_number = book_inv_number + 1 where book_ID = " + ID
    cursor.execute(sql)
    connection.commit()
    sql = "update card set card_br_now = card_br_now - 1 where card_ID = " + username
    cursor.execute(sql)
    connection.commit()
    now_date = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    sql = "insert into revert values(" + username + ", " + ID + ",'" + now_date + "')"
    cursor.execute(sql)
    connection.commit()
    sql = "update borrow set if_revert = 1 where if_revert = 0 and book_ID = " + ID + " LIMIT 1"
    cursor.execute(sql)
    connection.commit()

    sql = "select * from books"
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()

    sql = "select card_br_now from card where card_ID = " + username
    cursor.execute(sql)
    K = cursor.fetchall()
    for data in K:
        k = int(data['card_br_now'])
    connection.commit()
    sql = "select card_br_tot from card where card_ID = " + username
    cursor.execute(sql)
    M = cursor.fetchall()
    for data in M:
        m = int(data['card_br_tot'])
    connection.commit()
    return render_template('student.html', data_list=result, k=k, m=m)

@app.route('/change/<ID>')
def change_book(ID):
    global result
    for data in result :
        str_ID = str(data['book_ID'])
        if str_ID == ID:
            return render_template('change.html', user = data)

    return render_template('admin.html', data_list = result)

@app.route('/changed/<ID>', methods = ["POST"])
def changed_book(ID):
    global result
    ID2 = ""
    for data in result :
        str_ID = str(data['book_ID'])
        if str_ID == ID:
            ID2 = str(data['book_ID'])
            data['book_ID'] = request.form.get('book_ID')
            data['book_category'] = request.form.get('category')
            data['book_name'] = request.form.get('book_name')
            data['book_publisher'] = request.form.get('publisher')
            data['book_year'] = request.form.get('book_year')
            data['book_author'] = request.form.get('book_author')
            data['book_price'] = request.form.get('book_price')
            data['book_tot_number'] = request.form.get('tot_number')
            data['book_inv_number'] = request.form.get('book_inv_number')

    sql = "update books set book_ID = " + request.form.get('book_ID') + " where book_ID = " + ID2 + ';'
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_category = '" + request.form.get('category') + "' where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_name = '" + request.form.get('book_name') + "' where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_publisher = '" + request.form.get('publisher') + "' where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_year = " + request.form.get('book_year') + " where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_author = '" + request.form.get('book_author') + "' where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_price = " + request.form.get('book_price') + " where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_tot_number = " + request.form.get('tot_number') + " where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()
    sql = "update books set book_inv_number = " + request.form.get('book_inv_number') + " where book_ID = " + ID2
    cursor.execute(sql)
    connection.commit()

    sql = "select * from books"
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.commit()
    return render_template('admin.html', data_list = result)

@app.route('/query_user_list/<ID>')
def query_user_list(ID):
    sql = '''select book_ID, book_name, book_publisher, book_author, br_time
    from borrow natural join books 
    where if_revert = 0 and card_ID = ''' + ID
    cursor.execute(sql)
    query_result = cursor.fetchall()
    connection.commit()

    return render_template('query2.html', data_list = query_result, student_name = ID)

@app.route('/query')
def student_query():
    sql = '''select book_ID, book_name, book_publisher, book_author, br_time
    from borrow natural join books 
    where if_revert = 0 and card_ID = ''' + username
    cursor.execute(sql)
    query_result = cursor.fetchall()
    connection.commit()

    return render_template('query.html', data_list = query_result, student_name = username)

@app.route('/record')
def record():
    sql = '''select book_ID, book_name, book_publisher, book_author, br_time
    from borrow natural join books 
    where card_ID = ''' + username

    cursor.execute(sql)
    query_result = cursor.fetchall()
    connection.commit()
    for data in query_result:
        data['time'] = "借书"
        data['T'] = data['br_time']

    sql = '''select book_ID, book_name, book_publisher, book_author, re_time
        from revert natural join books 
        where card_ID = ''' + username
    cursor.execute(sql)
    query_result2 = cursor.fetchall()
    connection.commit()
    for data in query_result2:
        data['time'] = "还书"
        data['T'] = data['re_time']
    if query_result2 :
        Result = query_result + query_result2
    else :
        Result = query_result
    return render_template('record.html', data_list = Result, student_name = username)

@app.route('/query_user')
def query_user():
    sql = "select card_ID, card_password, card_br_tot, card_br_now from card where card_authority = 'student'"
    cursor.execute(sql)
    query_user = cursor.fetchall()
    connection.commit()

    return render_template('query_user.html', data_list = query_user)

@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

@app.route('/add_student2', methods = ['POST'])
def add_student2():
    name = request.form.get('username')
    word = request.form.get('password')
    num = request.form.get('number')
    sql = "insert into card values (" + name + ",'student','" + word + "'," + num + ", 0)"
    cursor.execute(sql)
    connection.commit()
    return render_template('admin.html', data_list = result)

@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

@app.route('/change_password2', methods = ['POST'])
def change_password2():
    global password
    old = request.form.get('old')
    new = request.form.get('new')

    if(old == str(password)):
        sql = "update card set card_password = " + new + " where card_ID = " + username
        print(sql)
        cursor.execute(sql)
        connection.commit()
        password = new

    sql = "select card_br_now from card where card_ID = " + username
    cursor.execute(sql)
    K = cursor.fetchall()
    for data in K:
        k = int(data['card_br_now'])
    connection.commit()
    sql = "select card_br_tot from card where card_ID = " + username
    cursor.execute(sql)
    M = cursor.fetchall()
    for data in M:
        m = int(data['card_br_tot'])
    connection.commit()
    return render_template('student.html', data_list=result, k=k, m=5)

@app.route('/add')
def book_add():
    return render_template('add.html')

@app.route('/add2', methods = ['POST'])
def book_add2():
    global result
    data = {}
    A = data['book_ID'] = request.form.get('book_ID')
    B = data['book_category'] = request.form.get('category')
    C = data['book_name'] = request.form.get('book_name')
    D = data['book_publisher'] = request.form.get('publisher')
    E = data['book_year'] = request.form.get('book_year')
    F = data['book_author'] = request.form.get('book_author')
    G = data['book_price'] = request.form.get('book_price')
    H = data['book_tot_number'] = request.form.get('tot_number')
    F = data['book_inv_number'] = request.form.get('book_inv_number')
    result.insert(0, data)

    sql = "insert into books values (" + A + ",'" + B + "','" + C + "','" + D + "'," + E + ",'" + F + "'," + G + "," + H + "," + F + ")"
    cursor.execute(sql)
    connection.commit()

    return render_template('admin.html', data_list = result)

if __name__ == '__main__':
    app.run()

#cursor.close()
#connection.close()