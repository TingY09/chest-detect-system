from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# 連接到 MongoDB，本地端 MongoDB URI 或使用 MongoDB Atlas 的 URI
client = MongoClient("mongodb://localhost:27017/")  # 本地
# client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority")  # MongoDB Atlas

# 選擇資料庫和集合
db = client['doctor']
collection = db['login']

@app.route('/add_user', methods=['POST'])
def add_user():
    # 從 POST 請求中取得 JSON 數據
    data = request.get_json()

    # 檢查是否有 name 和 email 欄位
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'msg': 'Missing name or email'}), 400

    # 構造插入到 MongoDB 的數據結構
    user = {
        'name': data['name'],
        'email': data['email']
    }

    # 插入數據到 login 集合
    result = collection.insert_one(user)
    
    # 返回插入成功的消息和新建文件的 _id
    return jsonify({'msg': 'User added', 'id': str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)