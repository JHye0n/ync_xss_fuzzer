#dev by, jhyeon(stjhyeon@kakao.com) & nga & seonghyun park
#!/usr/bin/python3

from core import *
import urllib.parse
from urllib.error import URLError, HTTPError
from flask import Flask,request,render_template,url_for,redirect
import re

app = Flask(__name__)

def check_url(url):
    try:
        regex = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if(url is not None):
            return regex.search(url).group(0)
    except:
        None

def vaild_url(url):
    url_scheme = urllib.parse.urlparse(url).scheme
    url_domain = urllib.parse.urlparse(url).hostname

@app.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET"])
def login_page():
    return '''login page'''

@app.route('/register', methods=["GET"])
def register_page():
    return '''register page'''

@app.route('/api/login', methods=["POST"])
def login():
    return '''login go'''

@app.route('/api/register', methods=["POST"])
def register():
    return '''register go'''

@app.route('/api/search', methods=["POST"])
def search():
    try:
        url = request.form.get('url')
        use_cookie = request.form.get('use_cookie')

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

    except HTTPError as e:
        return render_template('error/url_error.html')

    except ValueError as e:
        return render_template('error/url_error.html')

    except URLError as e:
        return render_template('error/url_error.html')

app.run('0.0.0.0',8000)
