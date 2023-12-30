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
    amount_of_articles=0
    user_orders=Order.query.filter_by(user_id=current_user.id, article_id=1).all()
    article_one=Article.query.filter_by(user_id=current_user.id, id=1).first()

    article_id_one_name = article_one.name
    print(article_id_one_name)

    for order in user_orders:
        amount_of_articles+=order.amount
    print(amount_of_articles)

    total_gains_id_one=amount_of_articles*article_one.price
    print(f'Total gains: {total_gains_id_one} Gs.')
            
    product_data_one= Product_data(article_name=article_id_one_name, sold_quantity=amount_of_articles, total_gains=total_gains_id_one)
    print(product_data_one)
    
    return render_template('statistics.html', amount_of_articles=amount_of_articles)




