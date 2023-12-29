
from flask_login import UserMixin
from services.database_service import db

class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    qr= db.relationship('QR', backref='owned', lazy='select')
    article=db.relationship('Article', backref='owned',lazy='select')
    order=db.relationship('Order', backref='owned',lazy='select')
    
'''     def __repr__(self):
        return '<User %r>' % self.name '''