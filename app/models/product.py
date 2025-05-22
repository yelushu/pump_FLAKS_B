from app import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    price1 = db.Column(DECIMAL(10, 2))  # 一级代理价
    price2 = db.Column(DECIMAL(10, 2))  # 二级代理价
    market_price = db.Column(DECIMAL(10, 2))
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    params = db.Column(db.Text)
    status = db.Column(db.Integer, default=1)  # 1-上架, 0-下架
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def to_dict(self, agent_level=0):
        data = {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'type': self.type,
            'brand': self.brand,
            'market_price': float(self.market_price) if self.market_price is not None else 0.0,
            'image_url': self.image_url,
            'description': self.description,
            'paramsparams': self.params,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'price1': float(self.price1) if self.market_price is not None else 0.0,
            'price2': float(self.price2) if self.market_price is not None else 0.0,
            "category_id":self.category_id
        }

        return data

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }