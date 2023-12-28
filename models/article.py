from services.database_service import db

class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    price=db.Column(db.Integer)
    url=db.Column(db.String(250))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    orders=db.relationship('Order', lazy='select')