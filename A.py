from flask import Flask
from login.routes import login_bp
from patients.routes import patient_bp
from patients.all import all_bp
from patients.revise import update_bp
from about.routes import about_bp
from detect.routes import detect_bp
from detect.predict import predict_bp

app = Flask(__name__)

# 註冊 Blueprint
app.register_blueprint(login_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(all_bp)
app.register_blueprint(update_bp)
app.register_blueprint(about_bp)
app.register_blueprint(detect_bp)
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    app.run(debug=True)

    # 可以在手機運作
    # app.run(port=5000, host='0.0.0.0')
