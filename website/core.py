#coding:utf-8
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_file, send_from_directory, make_response
from werkzeug.utils import secure_filename
from sql import *

import time
import os
import base64
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SECRET_KEY"] = "010016"
UPLOAD_FOLDER = "upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
#允许的文件类型
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'pdf', 'word', 'excel', 'ppt'])
tishiforindex = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#初始化sql类
sql = Sql('password')   # 此处改成自己的password

#文件上传函数
@app.route('/api/upload', methods = ['POST'], strict_slashes = False)
def api_upload():
    print('upload')
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'], session.get('userid'))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        # fpath = os.path.join(file_dir, fname)
        fpath = file_dir # 文件路径为文件所在文件夹
        try:
            print(fpath)
            sql.upload_file(fname, fpath)
        except HasnotSigninException as err:
            tishiforindex = "用户未登录！"
            return redirect(url_for('index'))
        else:
            f.save(os.path.join(file_dir, fname))
            tishiforindex = "上传成功！"
            return redirect(url_for('index'))
    else:
        tishiforindex = "文件格式不符合要求"
        return redirect(url_for('index'))

#文件下载函数
@app.route('/api/download/<filename>', methods = ['GET'])
def download_file(filename):
    directory = sql.select_file_path_by_name(filename)
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

#注册界面
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("registering")
        try:
            sql.sign_up(request.form['userid'], request.form['name'], request.form['password'])
        except AccountAlreadyExistError as err:
            return render_template('register.html', tishi = err)
        else:
            return redirect(url_for('login'))
    return render_template('register.html', tishi = None)

#登录界面
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            sql.sign_in(request.form['userid'], request.form['password'])
        except NoneAccountFoundError as err:
            return render_template('login.html', error = err, tishi = None)
        except MultAccountFoundError as err:
            return render_template('login.html', error = err, tishi = None)
        else:  
            session['userid'] = request.form['userid']
            return redirect(url_for('index'))
    return render_template('login.html', error = None, tishi = None)

#登出方法
@app.route('/logout')
def logout():
    sql.sign_out()
    session.pop('userid')
    return redirect(url_for('login'))

#主界面，若未登录则跳转到登录界面
@app.route('/')
def index():
    user_id = session.get('userid')
    if user_id == None:
        print('failure')
        return redirect(url_for('login'))
    user_name = sql.get_curent_user_name()
    fileids = sql.select_all_fileid()
    filelist = []
    for each in fileids:
        file = dict()
        filename = sql.select_file_name(each)
        print(sql.select_file_path(each))
        file['name'] = filename     # filename带后缀名
        file['postfix'] = filename.rsplit('.', 1)[1]
        filelist.append(file)
    return render_template('index.html', file = filelist, name = user_name, tishi = None)

if __name__ == '__main__':
    app.run()