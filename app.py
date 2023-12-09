from flask import Flask, render_template, request, url_for, redirect,send_file
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import qrcode
from io import BytesIO
import base64
import os
import zipfile
import secrets
import time
from datetime import datetime
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'chupetess'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'



class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    qr= db.relationship('QR', backref='owned', lazy='select')
    article=db.relationship('Article', backref='owned',lazy='select')
    
    def __repr__(self):
        return '<User %r>' % self.name
    
class QR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_first=db.Column(db.Boolean,default=False)
    party_name=db.Column(db.String(50))
    qr_data=db.Column(db.String(300))
    is_used=db.Column(db.Boolean,default=False)
    timestamp=db.Column(db.Integer)
    file_zip_name=db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    price=db.Column(db.Integer)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def primera():
    return redirect(url_for('index'))


@app.route('/login', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('input_qr'))
    return render_template('index.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        email = request.form['email']
        password=request.form['password']
        new_user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/update_status_qr/<string:qr_data>', methods=['POST','GET'])
@login_required
def update_status_qr(qr_data):
    token=qr_data
    qr_updated='False'
    # TODO HACER QUE SEA SOLO PARA EL CURRENT USER
    qr_row= QR.query.filter_by(qr_data=token).first()
    if qr_row:
        if qr_row.is_used==True:
            qr_updated='Used'
            return render_template('update_status.html',qr_updated=qr_updated)
        qr_row.is_used=True
        db.session.commit()
        qr_updated='True'
    return render_template('update_status.html',qr_updated=qr_updated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('register'))
    

@app.route('/generate_qr', methods=['POST','GET'])
@login_required
def generate_qr():
    data = f'{request.url_root}/update_status_qr/'
    num_qr = int(request.form.get('num_qr', 1))  # Número de QRs, por defecto 1
    party_name=request.form['party_name']
    is_first=True
    timestamp = datetime.now()
    zip_filename = f"entradas-qr-{timestamp}.zip"
    timestamp=timestamp.strftime("%d/%m/%y")
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for i in range(1, num_qr + 1):
            if i!=1:
                is_first=False
            # Generar un token único para cada QR
            token = secrets.token_urlsafe(16)

            
            # Crear el código QR
            qr_data = f"{data}/{token}_{i}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            new_qr=QR(qr_data=f'{token}_{i}',is_used=False,user_id=current_user.id,party_name=party_name,timestamp=timestamp,is_first=is_first,file_zip_name=zip_filename)
            db.session.add(new_qr)
            db.session.commit()

            # Crear una imagen PIL desde el código QR
            img = qr.make_image(fill_color="black", back_color="white")

            # Guardar la imagen en un archivo temporal
            img_bytes = BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)

            # Crear un archivo temporal para cada QR
            temp_filename = f"Entrada_numero_{party_name}_{i}.png"
            with open(temp_filename, 'wb') as temp_file:
                temp_file.write(img_bytes.read())

            # Agregar el archivo al zip
            zip_file.write(temp_filename, os.path.basename(temp_filename))

            # Eliminar el archivo temporal
            os.remove(temp_filename)

    # Enviar el archivo zip como una descarga
    return send_file(f'{zip_filename}', as_attachment=True, download_name=zip_filename)



@app.route('/download_qr', methods=['POST','GET'])
@login_required
def download_qr():
    list_of_all_qr = QR.query.filter(and_(QR.user_id == current_user.id, QR.is_first == True)).all()
    

    

    return render_template('download_qr.html',list_of_all_qr=list_of_all_qr, total_venta=total_venta)

@app.route('/add_product', methods=['GET','POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name=request.form['name']
        price=request.form['price']
        new_product=Article(name=name, price=price, user_id=current_user.id)
        db.session.add(new_product)
        db.session.commit()
    return render_template('add_product.html')

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    list_of_products=Article.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', list_of_products=list_of_products)


@app.route('/input_qr/<string:zip>', methods=['POST','GET'])
@login_required
def download_one_qr(zip):
    zip_file = zip
    return send_file(f'{zip_file}', as_attachment=True, download_name=zip_file)

    
@app.route('/input_qr')
def input_qr():
    return render_template('input_qr.html')


if __name__ == '__main__':
    app.run(debug=True)
