#!/usr/bin/python3

import re
from flask import Flask,request,render_template,url_for,redirect

app = Flask(__name__)

def check_url(url):
    try:
        regex = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if(url is not None):
            return regex.search(url).group(0)
        elif(url is None):
            return '''please input'''
    except:
        return '''error occured'''

@app.route('/', methods=["GET","POST"])
def index():
    # data save
    if request.method == 'POST':
        url = request.form.get('url')
        use_cookie = request.form.get('use_cookie')
    
        if(use_cookie is not None):
            cookie = request.form.get('cookie')
            if cookie and not cookie.isspace():
                url = check_url(url)
                return render_template('index.html', url=url, cookie=cookie)
            else:
                return '''cookie is none'''
        else:
            url = check_url(url)
            return render_template('index.html', url=url)

    if request.method == 'GET':
        return render_template('index.html')

app.run('0.0.0.0',8000)
