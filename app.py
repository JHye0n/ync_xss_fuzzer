#dev by, jhyeon(stjhyeon@kakao.com) & nga & seonghyun park
#!/usr/bin/python3

from core import *
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError
from flask import Flask,request,render_template,url_for,redirect,g
from passlib.hash import sha256_crypt
import re
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'

def vaild_url(url):
    url_scheme = urlparse(url).scheme
    url_domain = urlparse(url).netloc

    if(url_scheme != 'http','https'):
        return render_template('/error/url_error.html')

    if(url_domain == 'localhost' or '127.0.0.1' or ' '):
        return render_template('/error/url_error.html')

def load_db():
    if not hasattr(g, 'users.db'):
        db = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'users.db'):
      g.db.close()


@app.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET"])
def login_page():
    return render_template('login.html')

@app.route('/register', methods=["GET"])
def register_page():
    return render_template('register.html')

@app.route('/api/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    db = load_db()
    cursor = db.cursor()
    query = cursor.execute("SELECT * FROM users where username = ? AND password = ?", (username, sha256_crypt.encrypt(password))).fetchone()

    if query:
        return '''goood'''
    else:
        return '<script>alert("login failed"); history.go(-1); </script>'

@app.route('/api/register', methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    db = load_db()
    cursor = db.cursor()
    query = cursor.execute("SELECT * FROM users where username = ?", (username)).fetchone()

    if query:
        return '<script>alert("already exist account"); history.go(-1); </script>'
    else:
        query = "INSERT INTO users(username, password) VALUES (?,?)"
        query_exec = cursor.execute(query, (username, sha256_crypt.encrypt(password)))
        db.commit()
        return '''registeer ok'''

@app.route('/api/search', methods=["POST"])
def search():
    url = request.form.get('url')
    use_cookie = request.form.get('use_cookie')

    vaild_url(url)

    if(vaild_url is not None):
        if(use_cookie is not None):
            cookie = request.form.get('cookie')
            if cookie and not cookie.isspace():
                parser = XSsearch(url=url,cookies=cookie)
                parser.run()
                result = parser.result
                return render_template('index.html', result=result)
            else:
                return render_template('error/cookie_error.html')
        else:
            parser = XSsearch(url=url,cookies={})
            parser.run()
            result = parser.result
            return render_template('index.html', result=result)
    else:
        print('vaild url error')

app.run('0.0.0.0',8000)
