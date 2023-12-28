from controllers.user_controller import primera
from controllers.user_controller import login
from controllers.user_controller import register
from controllers.user_controller import logout
from flask import Blueprint

blueprint_user=Blueprint('blueprint_user', __name__)

blueprint_user.route('/', methods=['GET'])(primera)
blueprint_user.route('/login', methods=['GET','POST'])(login)
blueprint_user.route('/register', methods=['GET','POST'])(register)
blueprint_user.route('/logout', methods=['GET','POST'])(logout)
