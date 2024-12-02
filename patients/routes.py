from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 設定 MongoDB 連線
client = MongoClient('mongodb://localhost:27017')  # 或使用你的 MongoDB 連接字串
db = client['patient']  # 選擇資料庫名稱
patient_collection = db['data']  # 使用名為 "patients" 的資料表

# 儲存病患資料 API
@app.route('/save-patient-data', methods=['POST'])
def save_patient_data():
    try:
        # 從請求中取得 JSON 資料
        data = request.json
        
        # 如果存在 _id，則表示是更新現有資料
        if '_id' in data:
            patient_id = data['_id']
            del data['_id']  # 刪除 _id，因為 MongoDB 的 ObjectId 不能直接更新
            patient_collection.update_one({'_id': ObjectId(patient_id)}, {'$set': data})
            return jsonify({'message': '病患資料更新成功', 'status': 'success'})
        
        # 如果沒有 _id，則是新增資料
        result = patient_collection.insert_one(data)
        return jsonify({'message': '病患資料儲存成功', 'status': 'success', 'id': str(result.inserted_id)})
    
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'}), 500

# 獲取病患資料 API
@app.route('/get-patient-data/<patient_id>', methods=['GET'])
def get_patient_data(patient_id):
    try:
        # 根據 patient_id 查詢病患資料
        patient = patient_collection.find_one({'_id': ObjectId(patient_id)})
        if patient:
            patient['_id'] = str(patient['_id'])  # 轉換 ObjectId 為字串以便於傳輸
            return jsonify(patient)
        else:
            return jsonify({'message': '找不到病患資料', 'status': 'error'}), 404
    
    except Exception as e:
        return jsonify({'message': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
