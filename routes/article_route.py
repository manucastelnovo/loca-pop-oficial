from controllers.article_controller import add_product
from controllers.article_controller import products
from flask import Blueprint

blueprint_article=Blueprint('blueprint_article',__name__)

blueprint_article.route('/add_product', methods=['GET','POST'])(add_product)
blueprint_article.route('/products', methods=['GET', 'POST'])(products)

