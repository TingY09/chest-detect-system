from flask import Flask
from login.routes import login_bp, logout_bp
from patients.routes import get_bp, page_bp,  updateP_bp, add_bp, getP_bp
from patients.all import all_bp
from patients.revise import update_bp
from patients.diseasePic import patient_details_bp
from about.routes import about_bp
from detect.routes import detect_bp, save_bp
from detect.predict import predict_bp
from disease.route import diseaseAll_bp, diseaseName_bp
import os,secrets

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))  # 設定應用的 SECRET_KEY

# 註冊 Blueprint
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(get_bp)
app.register_blueprint(page_bp)
app.register_blueprint(updateP_bp)
app.register_blueprint(all_bp)
app.register_blueprint(update_bp)
app.register_blueprint(patient_details_bp)
app.register_blueprint(add_bp)
app.register_blueprint(getP_bp)
app.register_blueprint(about_bp)
app.register_blueprint(detect_bp)
app.register_blueprint(save_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(diseaseAll_bp)
app.register_blueprint(diseaseName_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

    # 可以在手機運作
    # app.run(port=5000, host='0.0.0.0')
    #執行指令：flask run --host=0.0.0.0 --app=A
 
