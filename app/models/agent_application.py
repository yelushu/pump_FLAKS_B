from app import db
from datetime import datetime
import bcrypt

class AgentApplication(db.Model):
    __tablename__ = 'agent_applications'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), unique=True)  # 微信唯一标识
    phone = db.Column(db.String(20), unique=True)
    password=db.Column(db.String(64),nullable=False)
    has_password=db.Column(db.String(255),nullable=False)
    company_name = db.Column(db.String(100))
    nickname = db.Column(db.String(64))  # 微信昵称
    avatar = db.Column(db.String(255))
    agent_level = db.Column(db.Integer, default=0)  # 0-普通用户, 1-一级代理, 2-二级代理
    address = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    user = db.relationship('User', backref='agent_applications')

    def to_dict(self):
        return {
            'id': self.id,
            'agent_level': self.agent_level,
            'company_name': self.company_name,
            'business_license': self.business_license,
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
            'address': self.address,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def set_password(password):
        salt = bcrypt.gensalt()
        has_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return has_password

    def check_password(self, password):
        print('进入验证')
        return bcrypt.checkpw(password.encode('utf-8'), self.has_password)



