from flask import Blueprint, render_template

# 定義一個 Blueprint
about_bp = Blueprint('about', __name__)

# 主頁路由，返回 HTML 頁面
@about_bp.route('/about')
def about():
    return render_template('about.html')  # 渲染前端頁面