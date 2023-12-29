from services.database_service import db

class Order(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    article_id=db.Column(db.Integer, db.ForeignKey('article.id'))
    amount=db.Column(db.Integer)
    list_of_orders_id=db.Column(db.Integer, db.ForeignKey('list_of_orders.id'))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
