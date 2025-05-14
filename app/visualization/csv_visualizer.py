import os
import csv
from flask import Blueprint, jsonify, render_template

csv_visualizer_bp = Blueprint('csv_visualizer', __name__)

@csv_visualizer_bp.route('/visualize/csv', methods=['GET'])
def visualize_csv():
    """读取本地 CSV 文件并返回可视化数据"""
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data.csv')  # 假设 CSV 文件名为 data.csv

    if not os.path.exists(csv_file_path):
        return jsonify({"success": False, "message": "CSV 文件不存在！"}), 404

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]
        return render_template('csv_visualizer.html', rows=rows)
    except Exception as e:
        return jsonify({"success": False, "message": f"读取 CSV 文件失败: {str(e)}"}), 500