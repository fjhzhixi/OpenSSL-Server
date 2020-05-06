from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from werkzeug.utils import secure_filename
from function import *

import time
import os
import base64

app = Flask(__name__)
app.config["SECRET_KEY"] = "010016"
UPLOAD_FOLDER = "upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

sys = Sql()
account_type = 0

@app.route('/test/upload')
def test_upload():
    return render_template('upload.html')

@app.route('/api/upload', methods = ['POST'], strict_slashes = False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        token = new_filename
        print('token='+token)
        return redirect(url_for('index'))
    else:
        return jsonify({"errno":1001, "errmsg": "上传失败"})

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        print("registering")
        user_id = sys.sign_up(int(request.form['type']), request.form['name'], request.form['password'])
        return render_template('login.html', error = None, tishi = 'user_' + user_id)
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            sys.sign_in(request.form['accout'][5:], request.form['password'])
        except NoneAccountFoundError as err:
            return render_template('login.html', error = err, tishi = None)
        except MultAccountFoundError as err:
            return render_template('login.html', error = err, tishi = None)
        else:  
            session['user_id'] = request.form['accout'][5:]
            session['user_type'] = str(sys.get_cur_account_type())
            return redirect(url_for('index'))

    return render_template('login.html', error = None, tishi = None)

@app.route('/logout')
def logout():
    sys.sign_out()
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/')
def index():
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    normal = 1
    if (user_type == "0"):
        normal = None
    provider = None
    if user_id == None:
        print('failure')
        return redirect(url_for('login'))
    print('continue')
    user_name = sys.get_cur_account_name()
    game = sys.select_game_id()
    games = []
    for each in game:
        ans = sys.select_game(each)
        p = sys.select_provider(str(ans['provider']))
        name = p['provider_name']
        ans['provider_name'] = name
        allgame = sys.select_owned_game_id()
        add = 0
        num = 0
        for one in allgame:
            if (str(one[1]) == str(ans['game_id'])):
                sea = sys.select_owned_game(str(one[0]), str(one[1]))
                if sea['game_evaluation'] != None:
                    add = add + sea['game_evaluation']
                    num = num + 1
        if num == 0:
            ans['evaluation'] = 100
        else:
            ans['evaluation'] = add/num
        games.append(ans)
    if (user_type == '2'):
        provider = 1
    return render_template('index.html', game = games, name = user_name, id = user_id, provider = provider, normal = normal)

if __name__ == '__main__':
    app.run(debug=True)