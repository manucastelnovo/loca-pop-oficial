from services.database_service import db


class List_of_orders(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    orders_access=db.relationship('Order', lazy='select')