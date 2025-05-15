from flask import Blueprint, render_template

bp = Blueprint('datacenter',__name__)

# 数据中心
@bp.route('/datacenter')
def datacenter():
    return render_template('datacenter.html')

# 数据库交互可视化界面
@bp.route('/visualization')
def visualization():
    return render_template('visualization.html')

# 数据中心分布
@bp.route('/distribution')
def distribution():
    return render_template('distribution.html')

# 数据总量
@bp.route('/total')
def total():
    return render_template('total.html')