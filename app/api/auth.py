from flask import jsonify, request
from app import db
from . import bp
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': '请提供用户名和密码'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'message': '用户名或密码错误'}), 401

    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.session.commit()

    # 生成JWT令牌
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    })

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户名已存在'}), 400

    user = User(
        username=data['username'],
        name=data.get('name'),
        phone=data.get('phone'),
        is_agent=data.get('is_agent', False),
        agent_level=data.get('agent_level', 0)
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '注册成功', 'user': user.to_dict()}), 201

@bp.route('/auth/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())