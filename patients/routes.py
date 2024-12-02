from flask import Blueprint, render_template, jsonify
from pymongo import MongoClient

# 定義一個 Blueprint
patient_bp = Blueprint('patient', __name__)

# 設定 MongoDB 連線
client = MongoClient('mongodb://localhost:27017')
db = client['patient']
patient_collection = db['data']

# 根據病患的姓名查詢資料，並渲染 patient.html
@patient_bp.route('/patient/<name>')
def get_patient_data(name):
    try:
        # 根據病患的姓名查詢 MongoDB 資料庫
        patient = patient_collection.find_one({'name': name})
        if patient:
            # 將病患資料傳遞給模板，並渲染 patient.html
            return render_template('patient.html', data=patient)
        else:
            return "找不到病患資料", 404
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'}), 500
