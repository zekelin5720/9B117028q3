import sqlite3

def db_init():
    """ 建立資料庫與資料表 """
    conn = sqlite3.connect('demo.db')
    conn.execute('''
        create table if not exists member
        (
            iid     integer primary key autoincrement,
            mnm     char(10) not null,
            mpwd    char(32) not null
        );
    ''')
    # 新增紀錄
    conn.execute("INSERT INTO member (mnm, mpwd) VALUES (?, ?)", ('test', '123456'))
    conn.commit()   # 將變動寫入檔案
    conn.close()
    return


def db_yn_query(id, pwd):
    conn = sqlite3.connect('demo.db')
    """ 查詢指定紀錄 """
    cursor = conn.execute("SELECT * FROM member WHERE mnm=? AND mpwd=?", (id, pwd))
    data = cursor.fetchall()
    conn.close()
    if len(data) > 0:
        return True
    return False