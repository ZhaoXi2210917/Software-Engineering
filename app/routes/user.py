# 这里定义用户相关的页面蓝图
from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)

# 加载用户相关的页面
@user_bp.route('/user/<page>')
def load_page(page):
    return render_template(f'{page}.html')