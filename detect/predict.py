from flask import Blueprint, request, jsonify
import torch
from torchvision import transforms
from PIL import Image
import io
import base64
# 定義一個 Blueprint
predict_bp = Blueprint('predict', __name__)

# 直接載入包含模型架構和權重的 .pth 檔案
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('train3modelefficientnet_b720.pth', map_location=device)
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

# 定義推論的路由
@predict_bp.route('/predict', methods=['POST'])
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
