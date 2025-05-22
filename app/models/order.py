from app import db
from datetime import datetime
from sqlalchemy import DECIMAL

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('agent_applications.id'), nullable=False)
    total_amount = db.Column(DECIMAL(10, 2), nullable=False)
    status = db.Column(db.Integer, default=0)  # 0-待支付, 1-已支付, 2-已发货, 3-已完成, 4-已取消
    address = db.Column(db.String(255))
    contact_name = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    remark = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    agent = db.relationship('AgentApplication', backref='orders')
    items = db.relationship('OrderItem', backref='orders', cascade='all, delete-orphan',lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'address': self.address,
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
            'remark': self.remark,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.price * self.quantity)
        }