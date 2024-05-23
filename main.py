from flask import Flask
from flask import request
from flask import render_template
from flask import url_for, redirect
from lib import *

app=Flask(__name__) # __name__ 代表目前執行的模組
db_init()

# flask利用裝飾器@app.route來定義路由，其後的裝飾(Decorator)通常是一個函數，用來提供執行的動作
@app.route("/")
def index():
    """ 路徑為 / 時所執行的程式 """
    return render_template('index.html')


# 表單與傳送方法(若不指定 methods 時，預設為 GET 方法)
@app.route("/login")
def login():
    """ 路徑為 /login 時所執行的程式 """
    return render_template('login.html')


@app.route("/show", methods=['GET', 'POST'])
def show():
    """ 路徑為 /show 時所執行的程式 """
    if request.method == 'POST':
        acc = request.form['username'].strip().lower()
        pwd = request.form['password'].strip().lower()
        result = db_yn_query(acc, pwd)
        if result:
            return render_template('show.html', username=acc)
        return render_template('msg.html', msg='Account/Password not correct')
    return render_template('index.html')