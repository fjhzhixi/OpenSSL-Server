from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from werkzeug.utils import secure_filename
from sql import *

import time
import os
import base64

app = Flask(__name__)
app.config["SECRET_KEY"] = "010016"
UPLOAD_FOLDER = "upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
tishiforindex = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

sys = Sql('xuqiang')    #此处修改数据库登录密码

@app.route('/api/upload', methods = ['POST'], strict_slashes = False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'], session.get('userid'))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        fpath = os.path.join(file_dir, fname)
        try:
            print(fpath)
            sys.upload_file(fname, fpath)
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

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("registering")
        try:
            sys.sign_up(request.form['userid'], request.form['name'], request.form['password'])
        except AccountAlreadyExistError as err:
            return render_template('register.html', tishi = err)
        else:
            return redirect(url_for('login'))
    return render_template('register.html', tishi = None)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            sys.sign_in(request.form['userid'], request.form['password'])
        except NoneAccountFoundError as err:
            return render_template('login.html', error = err, tishi = None)
        except MultAccountFoundError as err:
            return render_template('login.html', error = err, tishi = None)
        else:  
            session['userid'] = request.form['userid']
            return redirect(url_for('index'))
    return render_template('login.html', error = None, tishi = None)

@app.route('/logout')
def logout():
    sys.sign_out()
    session.pop('userid')
    return redirect(url_for('login'))

@app.route('/')
def index():
    user_id = session.get('userid')
    if user_id == None:
        print('failure')
        return redirect(url_for('login'))
    user_name = sys.get_curent_user_name()
    fileids = sys.select_all_fileid()
    filelist = []
    for each in fileids:
        file = dict()
        filename = sys.select_file_name(each)
        file['name'] = filename.rsplit('.', 1)[0]
        file['postfix'] = filename.rsplit('.', 1)[1]
        filelist.append(file)
    return render_template('index.html', file = filelist, name = user_name, tishi = None)

if __name__ == '__main__':
    app.run()