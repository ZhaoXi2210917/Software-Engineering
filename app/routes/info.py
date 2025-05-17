from flask import Blueprint, render_template,jsonify, request
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

# 获取鱼类重量
@bp.route('/getweight')
def get_weight():
    species = request.args.get('species', 'all')  # 默认值为 'all'
    # 连接数据库
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # 返回字典格式的结果
    # 执行查询
    if species == "all":
        cursor.execute("""
                SELECT weight 
                FROM fish 
            """)
    else:
        # 使用参数化查询
        query = """
                SELECT weight 
                FROM fish
                WHERE species = %s
            """
        cursor.execute(query, (species,))  # 将 species 作为参数传递
    # 获取结果
    results = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    # 提取宽度值
    weight_list = [row['weight'] for row in results]
    return jsonify(weight_list)

# 获取鱼类长度
@bp.route('/getlength')
def get_length():
    species = request.args.get('species', 'all')  # 默认值为 'all'
    # 连接数据库
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # 返回字典格式的结果
    # 执行查询
    if species == "all":
        cursor.execute("""
                SELECT length1 
                FROM fish 
            """)
    else:
        # 使用参数化查询
        query = """
                SELECT length1 
                FROM fish
                WHERE species = %s
            """
        cursor.execute(query, (species,))  # 将 species 作为参数传递
    # 获取结果
    results = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    # 提取宽度值
    length_list = [row['length1'] for row in results]
    return jsonify(length_list)

# 获取鱼类宽度
@bp.route('/getwidth')
def get_width():
    species = request.args.get('species', 'all')  # 默认值为 'all'
    # 连接数据库
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # 返回字典格式的结果
    # 执行查询
    if species == "all":
        cursor.execute("""
                SELECT width 
                FROM fish 
            """)
    else:
        # 使用参数化查询
        query = """
                SELECT width 
                FROM fish
                WHERE species = %s
            """
        cursor.execute(query, (species,))  # 将 species 作为参数传递
    # 获取结果
    results = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    # 提取宽度值
    width_list = [row['width'] for row in results]
    return jsonify(width_list)

# 获取水质信息
@bp.route('/getWaterData')
def get_water_data():
    # 连接数据库
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # 返回字典格式的结果
    cursor.execute("""
    SELECT temperature,ph,dissolved_oxygen,conductivity,turbidity,permanganate_index
    FROM water_data
    ORDER BY monitoring_time DESC
    LIMIT 1
    """)
    # 获取结果
    results = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    result = results[0]
    ordered_data = [
        result['ph'],
        result['temperature'],
        result['dissolved_oxygen'],
        result['conductivity'],
        result['turbidity'],
        result['permanganate_index']
    ]

    return ordered_data
# 主要信息
@bp.route('/info')
def info():
    # 鱼群种类信息 用于饼图
    raw_data = get_species()
    species_data = [{'name':item['species'],'value':item['count']} for item in raw_data]
    return render_template('info.html', species_data = species_data)

