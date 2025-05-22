from app import db
from app.models.product import Product, Category
from app.models.user import User

def init_db():
    # 创建管理员用户
    admin = User(
        username='admin',
        name='管理员',
        phone='13800138000',
        is_agent=True,
        agent_level=1
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # 创建产品分类
    categories = [
        Category(name='气动隔膜泵', description='各类气动隔膜泵产品'),
        Category(name='电动隔膜泵', description='各类电动隔膜泵产品'),
        Category(name='配件', description='隔膜泵配件')
    ]
    for category in categories:
        db.session.add(category)
    
    db.session.flush()  # 获取分类ID

    # 创建示例产品
    products = [
        {
            'name': 'QBY3-25 气动隔膜泵',
            'model': 'QBY3-25',
            'type': '气动',
            'brand': '某品牌',
            'price1': 1800.00,
            'price2': 2000.00,
            'market_price': 2500.00,
            'image_url': '/uploads/pump1.jpg',
            'description': '优质气动隔膜泵，适用于各种腐蚀性液体',
            'params': '[{"name":"口径","value":"25mm"},{"name":"流量","value":"3m³/h"},{"name":"压力","value":"0.7MPa"}]',
            'category_id': categories[0].id
        },
        {
            'name': 'DBY3-40 电动隔膜泵',
            'model': 'DBY3-40',
            'type': '电动',
            'brand': '某品牌',
            'price1': 2800.00,
            'price2': 3000.00,
            'market_price': 3500.00,
            'image_url': '/uploads/pump2.jpg',
            'description': '高效电动隔膜泵，节能环保',
            'params': '[{"name":"口径","value":"40mm"},{"name":"流量","value":"5m³/h"},{"name":"压力","value":"0.8MPa"}]',
            'category_id': categories[1].id
        }
    ]

    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)

    # 创建示例配件
    parts = [
        {
            'name': '隔膜片',
            'model': 'GM-25',
            'type': '配件',
            'brand': '某品牌',
            'price1': 100.00,
            'price2': 120.00,
            'market_price': 150.00,
            'image_url': '/uploads/part1.jpg',
            'description': '适用于QBY3-25型号隔膜泵',
            'params': '[{"name":"材质","value":"PTFE"},{"name":"尺寸","value":"25cm"}]',
            'category_id': categories[2].id
        },
        {
            'name': '气阀',
            'model': 'QF-25',
            'type': '配件',
            'brand': '某品牌',
            'price1': 200.00,
            'price2': 220.00,
            'market_price': 250.00,
            'image_url': '/uploads/part2.jpg',
            'description': '适用于QBY3系列隔膜泵',
            'params': '[{"name":"材质","value":"不锈钢"},{"name":"接口","value":"1寸"}]',
            'category_id': categories[2].id
        }
    ]

    for part_data in parts:
        part = Product(**part_data)
        db.session.add(part)

    db.session.commit()