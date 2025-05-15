from flask import Blueprint, render_template

bp = Blueprint('underwater',__name__)

# 水下系统
@bp.route('/underwater')
def underwater():
    return render_template('underwater.html')