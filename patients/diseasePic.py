from flask import Flask, request, jsonify, render_template, Blueprint
from pymongo import MongoClient
import gridfs
from io import BytesIO
import base64

patient_details_bp = Blueprint('patient_details', __name__)

# MongoDB 設置
client = MongoClient("mongodb://127.0.0.1:27017/")

# 指定資料庫和集合
patient_db = client["patient"]
data_collection = patient_db["data"]

disease_db = client["disease"]
disease_collection = disease_db["disease2"]
fs = gridfs.GridFS(disease_db)  # 初始化 GridFS 用於儲存圖片

# 儲存圖片至 GridFS
def save_image_to_db(image_data, filename):
    return fs.put(image_data, filename=filename)

# 病患詳情頁面
@patient_details_bp.route('/patient/<id_card>', methods=['GET'])
def patient_details(id_card):
    # 查詢病患基本資料
    patient_record = data_collection.find_one({"id_card_number": id_card})
    if not patient_record:
        return jsonify({"error": "病患資料不存在"}), 404

    # 查詢疾病紀錄並取得圖片
    disease_records = disease_collection.find({"patient_id": id_card})
    disease_info = []
    for record in disease_records:
        img_id = record.get("img_id")  # 取得已儲存的圖片 ID
        if img_id:
            grid_out = fs.get(img_id)  # 從 GridFS 取出圖片
            img_data = grid_out.read()
            img_b64 = base64.b64encode(img_data).decode('utf-8')  # 將圖片轉為 Base64 編碼以嵌入 HTML
            disease_info.append({
                "disease": record["disease"],
                "remark": record.get("remark", ""),
                "img_b64": img_b64
            })

    # 準備包含圖片的病患資料
    patient_info = {
        "name": patient_record.get("name", ""),
        "id_card": id_card,
        "height": patient_record.get("height", ""),
        "weight": patient_record.get("weight", ""),
        "birthday": patient_record.get("birthday", ""),
        "address": patient_record.get("address", ""),
        "disease_records": disease_info
    }

    return render_template("patientThis.html", data=patient_info)