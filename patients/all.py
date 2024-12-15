from flask import Blueprint, render_template, session, redirect, url_for, flash
from pymongo import MongoClient


# MongoDB 連線設定
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['patient']  # 使用你的資料庫名稱
patients_collection = db['data']  # 使用你的集合名稱

# 定義一個 Blueprint
all_bp = Blueprint('all', __name__)

# 主頁路由，返回 HTML 頁面
@all_bp.route('/all')
def all():
    if 'username' in session:
        # 從資料庫中取得所有病患的 id_card_number
        patients = list(patients_collection.find({}, {'_id': 0, 'id_card_number': 1}))
        return render_template('folder.html', username=session['username'], patients=patients)
    else:
        flash('請先登入。')
        return redirect(url_for('login.login'))