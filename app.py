#dev by, jhyeon(stjhyeon@kakao.com) & nga & seonghyun park
#!/usr/bin/python3

from core import *
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError
from flask import Flask,request,render_template,url_for,redirect,g,session,url_for
import re
import sqlite3
import hashlib
import os
import json

app = Flask(__name__, static_url_path="/static/", static_folder="./templates/static/")
DATABASE = 'users.db'
app.secret_key = os.urandom(24)

def vaild_url(url):

    url_scheme = urlparse(url).scheme
    url_domain = urlparse(url).netloc

    if(url_scheme == ''):
        return None

    if(url_domain == ''):
        return None

    if(url_scheme == 'http' or url_scheme == 'https'):
        if(url_domain == 'localhost' or url_domain == '127.0.0.1'):
            return None
        else:
            return url

def load_db():
    if not hasattr(g, 'users.db'):
        db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'users.db'):
      g.db.close()


@app.route('/', methods=["GET","POST"])
def index():
    if session.get('user') is not None:
        return render_template('main.html')
    else:
        return render_template('index.html')

@app.route('/login2', methods=["GET"])
def login2():
    return render_template('login.html')

@app.route('/login', methods=["GET"])
def login_page():
    if session.get('user') is not None:
        return render_template('main.html')
    else:
        return render_template('login.html')

@app.route('/logout', methods=["GET"])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/register', methods=["GET"])
def register_page():
    if session.get('user') is not None:
        return render_template('main.html')
    else:
        return render_template('register.html')

@app.route('/api/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    db = load_db()
    cursor = db.cursor()
    query = cursor.execute("SELECT * FROM users where username = ? AND password = ?", (username, hashlib.sha256(password.encode()).hexdigest())).fetchone()

    if query:
        session['user'] = query['username']
        return render_template('main.html')
    else:
        return '<script>alert("login failed"); history.go(-1); </script>'

@app.route('/api/register', methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    db = load_db()
    cursor = db.cursor()
    query = cursor.execute("SELECT * FROM users where username = ?", (username,)).fetchone()

    if query:
        return '<script>alert("already exist account"); history.go(-1); </script>'

    query2 = "INSERT INTO users(username, password) VALUES (?,?)"
    query_exec = cursor.execute(query2, (username, hashlib.sha256(password.encode()).hexdigest()))
    db.commit()
    return redirect(url_for('login_page'))

    if not query_exec:
        return '<script>alert("error occured"); history.go(-1); </script>'

@app.route('/api/search', methods=["POST"])
def search():
    url = request.form.get('url')
    use_cookie = request.form.get('use_cookie')

    check_url = vaild_url(url)
    if(check_url is not None):
        if(use_cookie is not None):
        #if(use_cookie == 'true'):
            cookie = request.form.get('cookie')
            if cookie and not cookie.isspace():
                parser = XSsearch(url=url,cookies=cookie)
                parser.run()
                result = parser.result
                return render_template('main.html', result=result)
            else:
                return render_template('error/cookie_error.html')
        else:
        #elif(use_cookie == 'false'):
            parser = XSsearch(url=url,cookies={})
            parser.run()
            return json.dumps(result)
    else:
        return render_template('error/url_error.html')

app.run('0.0.0.0',8000)
