from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
import torch
from torchvision import transforms
from PIL import Image
import io
import base64
from pymongo import MongoClient

app = Flask(__name__)

# 直接載入包含模型架構和權重的 .pth 檔案
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('model.pth', map_location=device)
model.eval()  # 設置為評估模式

# 定義 15 種類別
CLASSES = [
    'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
    'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass',
    'No Finding', 'Nodule', 'Pleural Thickening', 'Pneumonia', 'Pneumothorax'
]

# 定義預處理過程
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  # 調整圖像大小
    transforms.Grayscale(num_output_channels=3),  # 將灰階圖像轉換為 3 通道
    transforms.ToTensor(),  # 轉換為 Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # 正規化
])

# MongoDB 連接
client = MongoClient('mongodb://localhost:27017/')
db = client['doctor']
collection = db['login']

# 主頁路由，返回 HTML 頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['password']

        # 查詢資料庫中的使用者
        user = collection.find_one({'name': name, 'email': email})

        if user:
            # 若存在該使用者，跳轉至 bar.html
            return redirect(url_for('about'))
        else:
            # 若不存在，顯示錯誤訊息
            flash('登入失敗，請檢查您的名稱和電子郵件。')
            return render_template('login.html')

    return render_template('login.html')

# 主頁路由，返回 HTML 頁面
@app.route('/detect')
def detect():
    return render_template('bar.html')  # 渲染前端頁面

# 主頁路由，返回 HTML 頁面
@app.route('/about')
def about():
    return render_template('about.html')  # 渲染前端頁面

# 主頁路由，返回 HTML 頁面
@app.route('/patient')
def patient():
    return render_template('patient.html')  # 渲染前端頁面

# 處理按鈕按下後的邏輯，並跳轉到新頁面
@app.route('/go_to_home', methods=['POST'])
def go_to_new_page():
    return redirect(url_for('detect'))

# 定義推論的路由
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']

    # 將圖像轉換為 PIL 格式並進行預處理
    img = Image.open(file.stream)
    
    # 儲存原始圖像（後面會發送回前端）
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")  # 將圖像編碼成 base64
    
    # 預處理圖像並進行推論
    img_tensor = preprocess(img).unsqueeze(0)  # 增加 batch dimension
    img_tensor = img_tensor.to(device)  # 將圖像移動到 GPU（或 CPU）

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)

    # 使用模型預測值來選擇對應的類別名稱
    result = CLASSES[predicted.item()]
    
    # 返回結果和圖像
    return jsonify({'result': result, 'image': img_str})

if __name__ == '__main__':
    app.run(debug=True)
    # 可以在手機運作
    # app.run(port=5000, host='0.0.0.0')
