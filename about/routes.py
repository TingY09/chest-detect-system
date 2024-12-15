from flask import Blueprint, render_template, session, redirect, url_for, flash

# 定義一個 Blueprint
about_bp = Blueprint('about', __name__)

# 主頁路由，返回 HTML 頁面
@about_bp.route('/about')
def about():
    if 'username' in session:  # 檢查是否登入
        return render_template('about.html', username=session['username'])
    else:
        flash('請先登入。')
        return redirect(url_for('login.login'))