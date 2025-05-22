from app import create_app, db
from app.models.product import Product, Category
from app.models.user import User

app = create_app()
with app.app_context():
    # 创建分类
    cat1 = Category(name='气动隔膜泵', description='气动系列')
    cat2 = Category(name='电动隔膜泵', description='电动系列')
    db.session.add_all([cat1, cat2])
    db.session.commit()

    # 创建产品
    p1 = Product(name='QBY3-80 气动隔膜泵', model='QBY3-80', type='气动', brand='某品牌', price1=3999, price2=4200, market_price=4999, image_url='', description='高效气动隔膜泵', params='参数A', category_id=cat1.id)
    p2 = Product(name='DBY3-50 电动隔膜泵', model='DBY3-50', type='电动', brand='某品牌', price1=4599, price2=4800, market_price=5599, image_url='', description='高效电动隔膜泵', params='参数B', category_id=cat2.id)
    db.session.add_all([p1, p2])
    db.session.commit()

    # 创建用户
    u1 = User(username='admin', name='管理员', phone='13800000000')
    u1.set_password('admin123')
    db.session.add(u1)
    db.session.commit()

    print('模拟数据已插入')