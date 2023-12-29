from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from services.database_service import db


def login():
    if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/input_qr')
    return render_template('login.html')


def primera():
    return redirect('/login')


def register():
    if request.method == 'POST':
        name=request.form['name']
        email = request.form['email']
        password=request.form['password']
        new_user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


def logout():
    logout_user()
    return redirect('/register')

