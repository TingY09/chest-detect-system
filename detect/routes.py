from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask import request, jsonify
from bson import ObjectId
import base64
from datetime import datetime
import traceback
from pymongo import MongoClient
import os
import base64
from werkzeug.utils import secure_filename

def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# 定義一個 Blueprint
detect_bp = Blueprint('detect', __name__)
save_bp = Blueprint('save', __name__)

# MongoDB 連接
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['disease']
collection = db['disease2']



# 主頁路由，返回 HTML 頁面
@detect_bp.route('/detect')
def detect():
    if 'username' in session:  # 檢查是否登入
        return render_template('bar.html', username=session['username'])
    else:
        flash('請先登入。')
        return redirect(url_for('login.login'))
    
# 定義儲存圖片的資料夾
UPLOAD_FOLDER = 'static/uploads'

@save_bp.route('/save_data', methods=['POST'])
def save_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 取得其他資料
    patient_id = request.form.get('id_card')
    remark = request.form.get('remark')
    disease = request.form.get('disease')
    upload_time = request.form.get('upload_time')

    if not (patient_id and remark and upload_time):
        return jsonify({"error": "Missing required fields"}), 400

    # 儲存圖片至伺服器並生成檔案路徑
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # 儲存資料到 MongoDB
    patient_data = {
        "id_card": patient_id,
        "remark": remark,
        "disease": disease,
        "upload_time": datetime.strptime(upload_time, "%Y-%m-%dT%H:%M:%S.%fZ"),
        "image_path": file_path  # 儲存路徑而非Base64
    }
    collection.insert_one(patient_data)

    return jsonify({"message": "資料已成功儲存！", "image_path": file_path}), 200