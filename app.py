from flask import Flask, render_template, Response, redirect, request, session, abort, url_for, flash, current_app
import base64
import os
import mysql.connector
from werkzeug.utils import secure_filename
from datetime import date

app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    database="cloud_outsource"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM dr_user_reg WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['username'] = uname
            return redirect(url_for('user_home'))
        else:
            msg = 'Incorrect'
    return render_template('login.html', msg=msg)

@app.route('/user_reg', methods=['GET', 'POST'])
def user_reg():
    msg = ""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM dr_user_reg")
    maxid = mycursor.fetchone()[0]
    mycursor.close()
    if maxid is None:
        maxid = 1
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        uname = request.form['uname']
        pass1 = request.form['pass']
        cursor = mydb.cursor()
        today = date.today()
        rdate = today.strftime('%d-%m-%y')
        sql = "INSERT INTO dr_user_reg(id,name,contact,email,username,password,status,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, name, contact, email, uname, pass1, '0', rdate)
        cursor.execute(sql, val)
        mydb.commit()
        if cursor.rowcount == 1:
            msg = "success"
        else:
            msg = 'Failed'
        cursor.close()
    return render_template('user_reg.html', msg=msg)

@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    value = session.get('username', '')
    sample_string = "Cloud Based Data Server Security"
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return render_template('user_home.html', value=value)

@app.route('/user_view_file', methods=['GET', 'POST'])
def user_view_file():
    value = session.get('username', '')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dr_user_files WHERE to_user=%s', (value,))
    val = cursor.fetchall()
    cursor.close()
    return render_template('user_view_file.html', value=value, val=val)

@app.route('/user_upload_file', methods=['GET', 'POST'])
def user_upload_file():
    msg = ""
    value = session.get('username', '')
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dr_user_reg')
    udata = cursor.fetchall()
    cursor.close()
    if request.method == 'POST':
        file = request.files['file']
        upload = file.save(os.path.join("static\\upload", secure_filename(file.filename)))
        f1 = file.filename
        to_user = request.form['to_user']
        description = request.form['description']
        sample_string = f1
        sample_string_bytes = sample_string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        pb_key = base64_string[10:20]
        private_key = to_user
        prk_string_bytes = private_key.encode("ascii")
        base64_bytes = base64.b64encode(prk_string_bytes)
        base64_string1 = base64_bytes.decode("ascii")
        prt_key = base64_string1[5:15]
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM dr_user_files")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid = 1
        today = date.today()
        rdate = today.strftime('%d-%m-%y')
        sql = "INSERT INTO dr_user_files(id, uname, to_user, upload_file, description, pri_key, pub_key, status, file_st, rtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, value, to_user, f1, description, prt_key, pb_key, '0', base64_string, rdate)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
            msg = 'Upload_success'
        else:
            msg = 'Upload_failed'
        mycursor.close()
    return render_template('user_upload_file.html', udata=udata, msg=msg)

@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    return render_template('admin_home.html')

@app.route('/view_file', methods=['GET', 'POST'])
def view_file():
    act = ""
    uid = ""
    data = ""
    value = session.get('username', '')
    if request.method == 'POST':
        key = request.form['private_key']
        cursor1 = mydb.cursor()
        sql = 'SELECT * FROM dr_user_files WHERE pri_key=%s AND to_user=%s'
        cursor1.execute(sql, (key, value))
        data = cursor1.fetchall()
        cursor1.close()
        if data:
            action = "OK"
        else:
            action = "fake_key"
        return render_template('view_files.html', value=value, data=data, action=action)
    return render_template('view_files.html', value=value, data=data)

@app.route('/admin_login', methods=['GET', 'POST'])
def pro_index():
    msg = ""
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        cursor.fetchall()  # Fetch all results to avoid "Unread result found" error
        cursor.close()
        if account:
            session['username'] = uname
            return redirect(url_for('admin_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('admin_login.html', msg=msg)

@app.route('/admin_view_user', methods=['GET', 'POST'])
def admin_view_user():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dr_user_reg')
    data = cursor.fetchall()
    cursor.close()
    return render_template('admin_view_user.html', data=data)

@app.route('/admin_view_files', methods=['GET', 'POST'])
def admin_view_files():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM dr_user_files')
    val = cursor.fetchall()
    cursor.close()
    return render_template('admin_view_files.html', val=val)

@app.route('/adminlogout')
def prologout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/userlogout')
def uslogout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
