from flask import jsonify, request
from app import db
from . import bp
from app.models.product import Product, Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User


@bp.route('/search', methods=['GET'])
def search_products():
    try:
        keyword = request.args.get('keyword', '').strip()

        if not keyword:
            return jsonify({"status": 400, "error": "请输入搜索关键词"}), 400


        # 真实数据库查询
        results = Product.query.filter(
            db.or_(
                Product.name.ilike(f'%{keyword}%'),
                Product.model.ilike(f'%{keyword}%'),
                Product.description.ilike(f'%{keyword}%')
            )
        ).all()
        products_list = [product.to_dict() for product in results]


        # 获取用户代理等级（用于价格权限控制）还没实现功能
        # agent_level = get_agent_level_from_request(request)
        for i, product in enumerate(results, 1):
            print(f"{i}. ID:{product.id} 名称:{product.name} 型号:{product.model}")
        return jsonify({
            "status": 200,
            "data":  products_list
        })


    except Exception as e:

        return jsonify({"status": 500, "error": f"搜索失败ss: {str(e)}"}), 500

@bp.route('/productlist', methods=['GET'])
def get_product_list():
    category_id = request.args.get('category_id', type=int)
    print(category_id)
    if category_id:
        products = Product.query.filter_by(category_id=category_id)
    else:
        products = Product.query.all()
    products_list=[product.to_dict() for product in products]
    return jsonify({ "status": 200,  "data":  products_list  })


@bp.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')

    # 构建查询
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(
            db.or_(
                Product.name.like(f'%{search}%'),
                Product.model.like(f'%{search}%')
            )
        )

    # 获取用户代理等级
    agent_level = 0
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user:
                agent_level = user.agent_level
        except:
            pass

    # 分页
    pagination = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'items': [item.to_dict(agent_level) for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    try:
        results = Product.query.filter_by(id=id)

        # product=Product.to_dict(results)
        products_list = [product.to_dict() for product in results]

        return jsonify({ "status": 200, "data":  products_list})

    except Exception as e:

        return jsonify({"status": 500, "error": f"搜索失败ss: {str(e)}"}), 500


@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])