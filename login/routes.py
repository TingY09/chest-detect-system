from flask import Blueprint, render_template, request, redirect, url_for,flash,session
from pymongo import MongoClient
import os,secrets
import bcrypt

# 定義一個 Blueprint
login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)

login_bp.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))  # 用於 session 加密

# MongoDB 連接
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['doctor']
collection = db['login']

# 登入頁面路由
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查詢資料庫中的使用者
        user = collection.find_one({'username': username})

        hashed_password = user['password']

        # 將從資料庫讀取的字串密碼轉換回 bytes
        hashed_password_bytes = hashed_password.encode('utf-8')

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes):
                session['username'] = username  # 將使用者資料存入 session
                return redirect(url_for('about.about'))
            else:
                flash("密碼錯誤，請再試一次。")
        else:
            # 若不存在，顯示錯誤訊息
            flash('登入失敗，帳號不存在。')

    return render_template('login.html')

# 登出路由
@logout_bp.route('/logout')
def logout():
    session.pop('username', None)  # 移除 session 中的 username
    flash('您已成功登出。')
    return redirect(url_for('login.login'))
