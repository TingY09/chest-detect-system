from flask import Blueprint, render_template, jsonify,request, session, redirect, url_for, flash
from pymongo import MongoClient

# 定義一個 Blueprint
get_bp = Blueprint('get_patient_data', __name__)
page_bp = Blueprint('patient_page', __name__)
updateP_bp = Blueprint('update_patient', __name__)
add_bp = Blueprint('add_folder', __name__)
getP_bp = Blueprint('get_patient_images', __name__)



# MongoDB 連線設定
client = MongoClient('mongodb://127.0.0.1:27017/')
patient_db = client['patient']  # 使用你的資料庫名稱
patients_collection = patient_db['data']  # 使用你的集合名稱
disease_db = client['disease']  # 使用你的資料庫名稱
disease_collection = disease_db['disease2']  # 使用你的資料庫名稱

# 根據病患ID取得病患資料，顯示於patient.html
@get_bp.route('/patient/<id_card_number>', methods=['GET'])
def get_patient_data_and_images(id_card_number):
    try:
        # 查詢病患基本資料
        patient = patients_collection.find_one({'id_card_number': id_card_number}, {'_id': 0})
        if not patient:
            return jsonify({'status': 'error', 'message': '查無此病患資料'}), 404

        # 查詢病患疾病圖片資料
        records = list(disease_collection.find({"id_card": id_card_number}))

        disease_records = [
            {
                "image_path": record.get("image_path", ""),  # 傳遞圖片路徑
                "remark": record.get("remark", "無備註"),
                "disease": record.get("disease", "未知疾病"),
                "upload_time": record["upload_time"].strftime("%Y-%m-%d %H:%M:%S") if "upload_time" in record else "未知"
            }
            for record in records
        ]

        response = {
            "status": "success",
            "patient": patient,
            "disease_records": disease_records
        }

        if not disease_records:
            response["message"] = "No disease records found for this patient."

        return jsonify(response)

    except Exception as e:
        print(f"發生錯誤：{e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

    
# 渲染patient.html，並根據ID顯示對應資料
@page_bp.route('/patient')
def patient_page():
    # 從 URL 中取得 id_card_number
    id_card_number = request.args.get('id_card_number')
    
    # 根據 id_card_number 查詢病患資料
    patient = patients_collection.find_one({'id_card_number': id_card_number}, {'_id': 0})
    if 'username' in session:
        if patient:
            return render_template('patientThis.html', username=session['username'], data=patient)
        else:
            return "病患資料未找到", 404
    else:
        flash('請先登入。')
        return redirect(url_for('login.login'))


# 這是更新病患資料的路由
@updateP_bp.route('/update-patient', methods=['POST'])
def update_patient():
    data = request.json
    patient_id = data.get('id_card_number')
    
    if not patient_id:
        return jsonify({'status': 'error', 'message': 'ID缺失'}), 400

    # 更新病患資料
    updated_data = {
        'name': data['name'],
        'height': data['height'],
        'weight': data['weight'],
        'birthday': data['birthday'],
        'address': data['address']
    }
    
    # 查詢疾病紀錄並忽略 'No finding'
    disease_records = disease_collection.find({'id_card': patient_id})
    diseases = [record['disease'] for record in disease_records if record['disease'].lower() != 'no finding']
    updated_data['disease'] = ', '.join(set(diseases))  # 合併疾病名稱並去除重複

    result = patients_collection.update_one({'id_card_number': patient_id}, {'$set': updated_data})

    if result.matched_count > 0:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': '更新失敗或查無此病患'}), 404


@add_bp.route('/add_folder', methods=['POST'])
def add_folder():
    new_id_card_number = request.json.get('id_card_number')
    if not new_id_card_number:
        return jsonify({'error': '必須提供身份證號碼'}), 400

    # 新增病患資料，設置預設值以防止 null
    new_patient = {
        'name': '未填寫',
        'height': 0,
        'id_card_number': new_id_card_number,
        'weight': 0,
        'birthday': '未填寫',
        'address': '未填寫',
        'disease': '無紀錄'
    }
    patients_collection.insert_one(new_patient)
    return jsonify({'message': '成功新增資料夾', 'id_card_number': new_id_card_number}), 201



