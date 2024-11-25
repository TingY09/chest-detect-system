from flask import Blueprint, render_template, request, redirect, url_for,flash
from pymongo import MongoClient

# 定義一個 Blueprint
login_bp = Blueprint('login', __name__)

# MongoDB 連接
client = MongoClient('mongodb://localhost:27017/')
db = client['doctor']
collection = db['login']

# 主頁路由，返回 HTML 頁面
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['password']

        # 查詢資料庫中的使用者
        user = collection.find_one({'name': name, 'email': email})

        if user:
            # 若存在該使用者，跳轉至 bar.html
            return redirect(url_for('detect'))
        else:
            # 若不存在，顯示錯誤訊息
            flash('登入失敗，請檢查您的名稱和電子郵件。')
            return render_template('login.html')

    return render_template('login.html')
