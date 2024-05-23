from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
import logging

logging.basicConfig(level=logging.INFO,  # 設置記錄級別為 INFO
                    format='%(asctime)s - %(levelname)s - %(message)s',  # 設置日誌格式
                    filename='example.log',  # 設置日誌文件名
                    filemode='w')  # 設置寫入模式為覆蓋（覆蓋之前的日誌）



app = Flask(__name__)
app.secret_key = 'yo'

# 設定日誌級別為錯誤，將錯誤訊息寫入 error.log 檔
logging.basicConfig(filename='error.log', level=logging.ERROR)

# 資料庫初始化
def initialize_database():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS member
                 (indo TEXT PRIMARY KEY, pwd TEXT)''')
    # 插入測試資料
    c.execute("INSERT OR IGNORE INTO member VALUES ('test_indo', 'test_pwd')")
    conn.commit()
    conn.close()

# 初始化資料庫
#initialize_database()

@app.errorhandler(Exception)
def handle_error(error):
    # 寫入詳細錯誤訊息到日誌
    logging.exception("An error occurred: ")
    # 導向錯誤頁面
    return render_template('error.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        idno = request.form['username']
        pwd = request.form['password']
        # 連接資料庫
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM member WHERE idno=? AND pwd=?", (idno, pwd))
        member = c.fetchall()
        conn.close()
        

        if len(member) > 0:
            member = member[0]
            session['member'] = member
            return redirect(url_for('index'))
            
        else:
            error_message = "請輸入正確的帳號密碼"
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')
    

@app.route('/')
def index():
    #session.pop('member', None)
    if 'member' in session:
        member = session['member']
        return render_template('index.html',member=member,pagename="會員資料檢視")
    return render_template('login.html',pagename="首頁")

    '''
    
    if 'username' in session:
        #username = session['username']
        #member = session['member']
        #return render_template('index.html', username=username,member=member)
        return render_template('index.html', username=username,member=member)
    return render_template('login.html')

    if session['username'] != None:
        return render_template('index.html')
       

    if request.method == 'GET':
        member_str = request.args.get('member')
        member = member_str.split('!@#$')

        return render_template('index.html')
    elif request.method == 'POST':
        # 在這裡處理 POST 請求的邏輯
        # 例如，從表單中獲取數據並進行處理
        data = request.form['data']
        # 在此處對數據進行處理
        return redirect(url_for('success'))  # 重定向到成功頁面
    '''


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        u0 = request.form['u0']
        u1 = request.form['u1']
        u2 = request.form['u2']
        u3 = request.form['u3']
        u4 = request.form['u4']
        u5 = request.form['u5']
        u6 = request.form['u6']
        u7 = request.form['u7']
        
        # 連接資料庫
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        c.execute("update member set nm=?,birth=?,blood=?,phone=?,email=?,idno=?,pwd=? WHERE iid=?", (u1,u2,u3,u4,u5,u6,u7,u0))
        conn.commit()
        conn.close()
        
        member = list(session['member'])

        member[0] = request.form['u0']
        member[1] = request.form['u1']
        member[2] = request.form['u2']
        member[3] = request.form['u3']
        member[4] = request.form['u4']
        member[5] = request.form['u5']
        member[6] = request.form['u6']
        member[7] = request.form['u7']

        session['member'] = tuple(member)

        return redirect(url_for('index'))
    else:
        if 'member' in session:
            member = session['member']
            return render_template('edit.html',member=member,pagename="修改個人資訊")
        return render_template('login.html',pagename="首頁")



@app.route('/logout')
def logout():
    session.pop('member', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
