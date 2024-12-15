from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from pymongo import MongoClient


# MongoDB 連線設定
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['disease']  # 使用你的資料庫名稱
disease_collection = db['disease2']  # 使用你的集合名稱

# 定義一個 Blueprint
diseaseAll_bp = Blueprint('diseaseAll', __name__)
diseaseName_bp = Blueprint('diseaseName', __name__)

# 主頁路由，返回 HTML 頁面
@diseaseAll_bp.route('/diseaseAll')
def diseaseAll():
    if 'username' in session:
        # 從資料庫中取得所有病患的 id_card_number
        return render_template('diseaseFolder.html', username=session['username'], diseaseName=diseaseName)
    else:
        flash('請先登入。')
        return redirect(url_for('login.login'))
    

@diseaseName_bp.route('/disease/<diseaseName>', methods=['GET'])
def diseaseName(diseaseName):
    # 查詢 MongoDB，根據疾病名稱查找圖片路徑列表
    disease_data = disease_collection.find({'disease': diseaseName}, {'_id': 0, 'image_path': 1})

    # 將查詢結果轉為列表
    image_paths = [entry['image_path'] for entry in disease_data if 'image_path' in entry]

    if 'username' in session:
        # 將圖片路徑列表傳遞給前端
        return render_template('disease.html', diseaseName=diseaseName, username=session['username'], image_paths=image_paths)
    else:
        flash('請先登入。')
        return redirect(url_for('login.login'))

