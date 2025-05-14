import os
import json
from flask import Blueprint, jsonify, render_template

json_visualizer_bp = Blueprint('json_visualizer', __name__)

@json_visualizer_bp.route('/visualize/json', methods=['GET'])
def visualize_json():
    """读取本地 JSON 文件并返回可视化数据"""
    json_file_path = os.path.join(os.path.dirname(__file__), 'test.json')

    # 打印调试信息
    print(f"JSON 文件路径: {json_file_path}")
    print(f"文件是否存在: {os.path.exists(json_file_path)}")

    if not os.path.exists(json_file_path):
        return jsonify({"success": False, "message": "JSON 文件不存在！"}), 404

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 检查模板文件是否存在
        template_path = os.path.join(os.getcwd(), 'app/templates/json_visualizer.html')
        print(f"模板路径: {template_path}")
        if not os.path.exists(template_path):
            return jsonify({"success": False, "message": "模板文件不存在！"}), 500

        return render_template('json_visualizer.html', data=json.dumps(data, ensure_ascii=False, indent=4))
    except Exception as e:
        return jsonify({"success": False, "message": f"读取 JSON 文件失败: {str(e)}"}), 500