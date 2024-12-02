from flask import Blueprint, render_template, jsonify
from pymongo import MongoClient

# 定義一個 Blueprint
all_bp = Blueprint('all', __name__)

# 主頁路由，返回 HTML 頁面
@all_bp.route('/all')
def all():
    return render_template('folder.html')  # 渲染前端頁面


