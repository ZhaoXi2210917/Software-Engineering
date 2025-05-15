from flask import Blueprint, render_template,jsonify
import mysql.connector
import json
from config import DB_CONFIG

bp = Blueprint('info',__name__)

# 获取种类信息
def get_species():
    # 连接数据库
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # 返回字典格式的结果
    # 执行查询
    cursor.execute("""
        SELECT species, COUNT(*) AS count 
        FROM fish 
        GROUP BY species
        ORDER BY count DESC
    """)
    # 获取结果
    results = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    return results

# 主要信息
@bp.route('/info')
def info():
    species_data = get_species()
    species_json = json.dumps(species_data)
    return render_template('info.html', species_data = species_json)

# @bp.route('/pie-data')
# def pie_data():
#     species_data = get_species()
#     return jsonify(species_data)

# if __name__ == '__main__':
#     result = get_species()
#     print(type(result))
#     for row in result:
#         print(f"种类：{row['species']}数量：{row['count']}")