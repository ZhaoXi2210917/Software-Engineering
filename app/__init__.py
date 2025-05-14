# app/__init__.py
from flask import Flask
from app.routes.auth import auth_bp  # 导入 auth 蓝图
from app.routes.main import bp as main_bp   # 导入 main 蓝图
from app.visualization.json_visualizer import json_visualizer_bp # 可视化TODO
from app.visualization.csv_visualizer import csv_visualizer_bp # 可视化TODO
from app.routes.user import user_bp  # 导入 user 蓝图 
from app.routes.admin import admin_bp  # 导入 admin 蓝图


def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)  
    app.register_blueprint(json_visualizer_bp)
    app.register_blueprint(csv_visualizer_bp)
    app.register_blueprint(user_bp)  
    app.register_blueprint(admin_bp)
    
    return app