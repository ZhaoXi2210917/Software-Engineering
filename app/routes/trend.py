from flask import Blueprint, jsonify
import datetime
import random

bp = Blueprint('trend', __name__)

@bp.route('/api/trend_data')
def get_trend_data():
    # 模拟生成7天的预测数据
    today = datetime.date.today()
    timestamps = [(today + datetime.timedelta(days=i)).isoformat() for i in range(7)]
    values = [round(0.5 + i * 0.1 + random.uniform(-0.05, 0.05), 2) for i in range(7)]

    return jsonify({'timestamps': timestamps, 'values': values})


@bp.route('/api/suggestions')
def get_suggestions():
    # 简单逻辑：模拟建议
    suggestion = "根据预测数据，预计5天内鱼体重将达到上市标准，请提前做好销售准备。"
    return jsonify({'suggestion': suggestion})
