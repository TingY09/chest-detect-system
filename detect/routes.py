from flask import Blueprint, render_template

# 定義一個 Blueprint
detect_bp = Blueprint('detect', __name__)

# 主頁路由，返回 HTML 頁面
@detect_bp.route('/detect')
def detect():
    return render_template('bar.html')  # 渲染前端頁面