from flask import Blueprint, redirect, render_template,url_for

# 如果页面提示找不到，可以在这里注册路由，可以在这里添加新的路由
# 或者在这个目录下新建文件

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/admin.html')
def admin():
    return render_template('admin.html')

@bp.route('/dashboard.html')
def dashboard():
    # 跳转到 user 蓝图的控制台页面
    # return redirect(url_for('user.load_page', page='dashboard'))
    return render_template('dashboard.html')

