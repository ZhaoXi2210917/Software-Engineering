# app/routes/auth.py
from flask import Blueprint, request, jsonify
import pymysql
from config import DB_CONFIG  # 从 config.py 导入数据库配置

auth_bp = Blueprint('auth', __name__)  # 创建 Blueprint

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空！"}), 400

    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # 查询用户信息
        query = "SELECT id, username, role FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "success": True,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"]
                },
                "is_admin": user["role"] == "admin"
            })
        else:
            return jsonify({"success": False, "message": "用户名或密码错误！"}), 401

    except Exception as e:
        print("数据库查询失败:", e)
        return jsonify({"success": False, "message": "服务器内部错误！"}), 500

    finally:
        if 'connection' in locals():
            connection.close()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')  # 新增 email 字段
    role = data.get('role', 'user')  # 默认角色为普通用户

    if not username or not password or not email:
        return jsonify({"success": False, "message": "用户名、密码和邮箱不能为空！"}), 400

    try:
        # 连接数据库
        with pymysql.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                # 检查用户名是否已存在
                check_query = "SELECT id FROM users WHERE username=%s"
                cursor.execute(check_query, (username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    return jsonify({"success": False, "message": "用户名已存在！"}), 400

                # 插入新用户（直接使用明文密码）
                insert_query = "INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (username, password, email, role))
                connection.commit()

        return jsonify({"success": True, "message": "注册成功！"}), 201

    except Exception as e:
        print("数据库操作失败:", e)
        return jsonify({"success": False, "message": "服务器内部错误！"}), 500