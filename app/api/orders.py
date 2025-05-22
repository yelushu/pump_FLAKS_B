from flask import jsonify, request
from app import db
from . import bp
from app.models.order import Order, OrderItem
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

@bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()

    # 验证数据
    if not data.get('items') or not data.get('address'):
        return jsonify({'message': '缺少必要参数'}), 400

    try:
        # 创建订单
        order = Order(
            user_id=user_id,
            total_amount=0,
            address=data['address'],
            contact_name=data['contact_name'],
            contact_phone=data['contact_phone'],
            remark=data.get('remark', '')
        )
        db.session.add(order)
        db.session.flush()  # 获取order.id

        # 添加订单项
        total_amount = 0
        for item in data['items']:
            product = Product.query.get_or_404(item['product_id'])
            
            # 根据用户代理等级获取价格
            user = order.user
            price = product.price1 if user.agent_level == 1 else product.price2
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item['quantity'],
                price=price
            )
            db.session.add(order_item)
            total_amount += float(price) * item['quantity']

        # 更新订单总金额
        order.total_amount = total_amount
        db.session.commit()

        return jsonify(order.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '创建订单失败'}), 500

@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', type=int)

    # 构建查询
    query = Order.query.filter_by(user_id=user_id)
    if status is not None:
        query = query.filter_by(status=status)

    # 按创建时间倒序排序
    query = query.order_by(Order.created_at.desc())

    # 分页
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': [order.to_dict() for order in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify(order.to_dict())

@bp.route('/orders/<int:id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()

    if order.status != 0:
        return jsonify({'message': '只能取消待支付的订单'}), 400

    order.status = 4  # 已取消
    order.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(order.to_dict())

@bp.route('/orders/<int:id>/pay', methods=['POST'])
@jwt_required()
def pay_order(id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()

    if order.status != 0:
        return jsonify({'message': '订单状态错误'}), 400

    # TODO: 实现支付逻辑

    # 更新订单状态
    order.status = 1  # 已支付
    order.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify(order.to_dict())