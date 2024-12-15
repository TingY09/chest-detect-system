from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# 定義一個 Blueprint
update_bp = Blueprint('update', __name__)

# MongoDB 連線 (請根據需求調整)
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['patient']  # 使用你的資料庫名稱
collection = db['data']  # 使用你的集合名稱

@update_bp.route('/api/update-patient', methods=['POST'])
def update_patient():
    data = request.get_json()
    
    # 確保 id_card_number 是字串
    patient_id = str(data.get('id_card_number'))  # 確保身分證字號以字串形式處理
    print(f"Received patient_id: {patient_id}")

    # 檢查病患資料是否存在
    existing_patient = collection.find_one({'id_card_number': patient_id})
    print(f"Existing patient data: {existing_patient}")

    if existing_patient is None:
        return jsonify({'status': 'error', 'message': '找不到病患資料'})

    # 進行更新操作
    result = collection.update_one(
        {'id_card_number': patient_id},
        {'$set': {
            'name': data.get('name'),
            'height': data.get('height'),
            'weight': data.get('weight'),
            'birthday': data.get('birthday'),
            'address': data.get('address'),
            'disease': data.get('disease')
        }}
    )

    print(f"Matched count: {result.matched_count}")
    print(f"Modified count: {result.modified_count}")

    if result.matched_count:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': '資料未更新'})