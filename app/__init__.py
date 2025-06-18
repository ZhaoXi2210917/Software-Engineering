# app/__init__.py
from flask import Flask
from app.routes.auth import auth_bp  # 导入 auth 蓝图
from app.routes.main import bp as main_bp   # 导入 main 蓝图
from app.visualization.json_visualizer import json_visualizer_bp # 可视化TODO
from app.visualization.csv_visualizer import csv_visualizer_bp # 可视化TODO

from app.routes.admin import admin_bp  # 导入 admin 蓝图
from app.routes.info import bp as info_bp   # 主要信息蓝图
from app.routes.underwater import bp as underwater_bp   # 水下系统蓝图
from app.routes.smartcenter import bp as smartcenter_bp # 智能中心蓝图
from app.routes.datacenter import bp as datacenter_bp   # 数据中心蓝图
from app.routes.trend import bp as trend_bp  # 养殖趋势蓝图



def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)  
    app.register_blueprint(json_visualizer_bp)
    app.register_blueprint(csv_visualizer_bp)

    app.register_blueprint(admin_bp)
    app.register_blueprint(info_bp)
    app.register_blueprint(underwater_bp)
    app.register_blueprint(smartcenter_bp)
    app.register_blueprint(datacenter_bp)
    app.register_blueprint(trend_bp)
    
    return app