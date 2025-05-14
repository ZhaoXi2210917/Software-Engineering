# 这里定义用户相关的页面蓝图
from flask import Blueprint, jsonify, render_template
import pymysql
from config import DB_CONFIG  # 从 config.py 导入数据库配置

admin_bp = Blueprint('admin', __name__)

# 加载用户相关的页面
@admin_bp.route('/admin/<page>')
def load_page(page):
    return render_template(f'{page}.html')

# 获取用户列表
@admin_bp.route('/admin/users', methods=['GET'])
def get_users():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # 查询所有用户
        query = "SELECT id, username, role FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        return jsonify({"success": True, "users": users})
    except Exception as e:
        print("数据库查询失败:", e)
        return jsonify({"success": False, "message": "服务器内部错误！"}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# 删除用户
@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # 删除用户
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        connection.commit()

        return jsonify({"success": True, "message": "用户已删除！"})
    except Exception as e:
        print("删除用户失败:", e)
        return jsonify({"success": False, "message": "服务器内部错误！"}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# 切换用户角色
@admin_bp.route('/admin/users/<int:user_id>/toggle-role', methods=['PUT'])
def toggle_role(user_id):
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # 获取当前用户角色
        query = "SELECT role FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "message": "用户不存在！"}), 404

        # 切换角色
        new_role = "admin" if user["role"] == "user" else "user"
        update_query = "UPDATE users SET role = %s WHERE id = %s"
        cursor.execute(update_query, (new_role, user_id))
        connection.commit()

        return jsonify({"success": True, "message": "用户角色已更新！", "new_role": new_role})
    except Exception as e:
        print("切换用户角色失败:", e)
        return jsonify({"success": False, "message": "服务器内部错误！"}), 500
    finally:
        if 'connection' in locals():
            connection.close()