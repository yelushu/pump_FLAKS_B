from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 3600  # 24 hours
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')

    # 确保上传目录存在
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)  # 需要有效 JWT 才能访问
    migrate.init_app(app, db) # 绑定 Flask 应用和数据库实例
    CORS(app)

    # 注册Flask-Admin
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    from .models.product import Product, Category#显式导出模型类：
    from .models.user import User
    from .models.agent_application import AgentApplication
    from .models.order import Order
    admin = Admin(app, name='管理后台', template_mode='bootstrap4')
    admin.add_view(ModelView(Product, db.session, name='产品'))
    admin.add_view(ModelView(Category, db.session, name='分类'))
    admin.add_view(ModelView(User, db.session, name='用户'))
    admin.add_view((ModelView(AgentApplication, db.session,name='代理信息')))
    admin.add_view((ModelView(Order, db.session,name='订单')))
    # 下面这段代码会自动补全数据库缺失的表
    # with app.app_context():
    #     db.create_all()

        # 注册蓝图
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    return app