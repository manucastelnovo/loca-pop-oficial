from flask import Flask
from routes.user_route import blueprint_user
from routes.article_route import blueprint_article
from routes.qr_route import blueprint_qr
from services.database_service import db
from services.login_manager_service import login_manager

def create_app():
    app=Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    return app

app=create_app()
app.register_blueprint(blueprint_user)
app.register_blueprint(blueprint_qr)
app.register_blueprint(blueprint_article)

login_manager.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
