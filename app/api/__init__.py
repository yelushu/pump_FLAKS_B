from flask import Blueprint
from flask import jsonify, request
# 核心修复：确保蓝图对象名称与注册时一致
bp = Blueprint('api', __name__)

# 延迟导入路由（避免循环引用）
from . import products, auth, orders, upload,agent  # 按需导入您的路由文件
