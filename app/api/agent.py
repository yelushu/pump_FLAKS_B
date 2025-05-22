from flask import jsonify, request
from app import db
from . import bp
from app.models.agent_application import AgentApplication
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime


@bp.route('/agent/apply', methods=['POST'])
@jwt_required()# 添加此装饰器
def apply_agent():
    data = request.get_json()

    user_id = get_jwt_identity() # 获取当前用户ID（从JWT中提取）

    user = User.query.get_or_404(user_id)

    # 检查是否已经是代理
    if user.is_agent:
        return jsonify({'message': '您已经是代理商'}), 400

    # 检查是否有待审核的申请
    pending_application = AgentApplication.query.filter_by(
        user_id=user_id,
        status=0
    ).first()
    if pending_application:
        return jsonify({'message': '您有待审核的申请'}), 400

    try:
        # 创建代理申请
        application = AgentApplication(
            user_id=user_id,
            agent_level=data['agent_level'],
            company_name=data['company_name'],
            business_license=data['business_license'],
            contact_name=data['contact_name'],
            contact_phone=data['contact_phone'],
            address=data['address']
        )
        db.session.add(application)
        db.session.commit()

        return jsonify(application.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '申请提交失败'}), 500

@bp.route('/agent/applications', methods=['GET'])
@jwt_required()
def get_applications():
    user_id = get_jwt_identity()
    applications = AgentApplication.query.filter_by(user_id=user_id)\
        .order_by(AgentApplication.created_at.desc()).all()
    return jsonify([app.to_dict() for app in applications])

@bp.route('/agent/upgrade', methods=['POST'])
@jwt_required()
def apply_upgrade():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    # 检查当前代理等级
    if not user.is_agent:
        return jsonify({'message': '您还不是代理商'}), 400
    if user.agent_level == 1:
        return jsonify({'message': '您已经是最高等级代理'}), 400

    # 检查是否有待审核的申请
    pending_application = AgentApplication.query.filter_by(
        user_id=user_id,
        status=0
    ).first()
    if pending_application:
        return jsonify({'message': '您有待审核的申请'}), 400

    try:
        # 创建升级申请
        application = AgentApplication(
            user_id=user_id,
            agent_level=1,  # 升级到一级代理
            company_name=data['company_name'],
            business_license=data['business_license'],
            contact_name=data['contact_name'],
            contact_phone=data['contact_phone'],
            address=data['address']
        )
        db.session.add(application)
        db.session.commit()

        return jsonify(application.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '申请提交失败'}), 500


@bp.route('/agent/phone-login', methods=['POST'])
# @jwt_required()# 添加此装饰器
def phone_login():
    data = request.get_json()
    print(data)
    phone = data.get('phone')
    password = data.get('password')

    # 参数验证
    if not phone or not password:
        return jsonify({'code': 400, 'message': '手机号和密码必填'}), 400

    # 查找用户
    user = AgentApplication.query.filter_by(phone=phone).first()
    is_new = False

    # 自动注册逻辑
    if not user:
        new_password=AgentApplication.set_password(password=password)
        user = AgentApplication(
            phone=phone,
            password=password,
            has_password=new_password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'code': 200,
            'user': {
                'id': user.id,
                'is_new': 1,
                'agent_level': user.agent_level
            }
        })

    else:
        # 验证密码
        if password!=user.password:
            return jsonify({'code': 401, 'message': '密码错误'}), 401
        else:
            return jsonify({
                'code': 200,
                'user': {
                    'id': user.id,
                    'is_new':0,
                    'agent_level': user.agent_level
                }
            }) ,print(user)

@bp.route('/agent/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    phone = data.get('phone')
    new_password = data.get('new_password')

    if not phone or not new_password:
        return jsonify({'code': 400, 'message': '手机号和新密码必填'}), 400

    user = AgentApplication.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    # 设置新密码
    user.password = new_password
    user.has_password = AgentApplication.set_password(new_password)
    db.session.commit()
    return jsonify({'code': 200, 'message': '密码重置成功'})

@bp.route('/agent/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    phone = data.get('phone')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not phone or not old_password or not new_password:
        return jsonify({'code': 400, 'message': '参数不完整'}), 400

    user = AgentApplication.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    # 校验旧密码
    if not user.check_password(old_password):
        return jsonify({'code': 401, 'message': '旧密码错误'}), 401

    # 设置新密码
    user.password = new_password
    user.has_password = AgentApplication.set_password(new_password)
    db.session.commit()
    return jsonify({'code': 200, 'message': '密码修改成功'})

