import os
from flask import Flask
from .models import db
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    
    # 載入基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)
    
    # 資料庫設定 (SQLite)
    db_path = os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化套件
    db.init_app(app)
    
    # 註冊路由 Blueprint
    register_routes(app)
    
    # 在啟動時自動建立資料庫表
    with app.app_context():
        db.create_all()
        
    return app
