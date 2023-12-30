from flask import render_template, request
from flask_login import current_user
from models.article import Article
from models.order import Order
from models.product_data import Product_data
from models.list_of_orders import List_of_orders
from services.database_service import db

def add_product():
    if request.method == 'POST':
        name=request.form['name']
        price=request.form['price']
        url=request.form['url']
        new_product=Article(name=name, price=price, user_id=current_user.id, url=url)
        db.session.add(new_product)
        db.session.commit()
    return render_template('add_product.html')

def products():
    if request.method == 'POST':
        new_list_of_orders=List_of_orders()
        db.session.add(new_list_of_orders)
        db.session.commit()
    # Aquí obtienes todos los datos enviados desde el formulario
        product_data = request.form.to_dict(flat=False)
        # Puedes iterar sobre los datos y mostrar tanto el nombre como el valor
        for field_name, field_values in product_data.items():
            new_order=Order(user_id=current_user.id,article_id=int(field_name), amount=int(field_values[0]), list_of_orders_id=new_list_of_orders.id)
            db.session.add(new_order)
            db.session.commit()
            
    list_of_products=Article.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', list_of_products=list_of_products)

def statistics():

    list_of_row=[]
    list_of_article=Article.query.filter_by(user_id=current_user.id).all()

    for Art in list_of_article:
        total_amount=0
        orders_of_articles=Order.query.filter_by(article_id=Art.id).all()
        for order in orders_of_articles:
            total_amount+=order.amount
        total_sold=total_amount*Art.price
        art_name=Art.name
        list_of_row.append(Product_data(article_name=art_name,sold_quantity=total_amount,total_gains=total_sold))
    return render_template('statistics.html',list_of_row=list_of_row)


