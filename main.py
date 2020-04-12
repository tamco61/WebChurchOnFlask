from flask import Flask, render_template, redirect, request, abort, url_for
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import PasswordField, TextAreaField, StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask import jsonify, make_response
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from data import db_session
from data.users import User
from data.products import Product
from data.sales import Sale
from requests import get, delete, post, put

import geocode
import products_api
import sales_api

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/database.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)


class AdminMixin:
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.privileges

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, 'Flask', url='/', index_view=HomeAdminView(name='Home'))
session = db_session.create_session()
admin.add_view(AdminView(User, session))
admin.add_view(AdminView(Product, session))
admin.add_view(AdminView(Sale, session))


@app.errorhandler(404)
def not_found(error):
    return render_template('err404.html', title='404')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    submit = SubmitField('Зарегиcтрироваться')


@app.route('/')
def index():
    return render_template("index.html", title='Главная страница')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/contacts')
def cont():
    return render_template('contacts.html', title='Контакты')


@app.route('/store')
def store():
    session = db_session.create_session()
    lst = session.query(Product).all()
    sales = session.query(Sale).all()
    sales = [i.item for i in sales]
    price_lst = list()
    if lst:
        for i in lst:
            if i.id in sales:
                continue
            ls = list()
            user = session.query(User).filter(User.id == i.seller).first()
            ls.append(i.id)
            ls.append(i.name)
            ls.append((user.surname, user.name))
            ls.append(i.price)
            price_lst.append(ls)
    return render_template('store.html', title='Магазин', price_lst=price_lst)


@app.route('/order/<int:id>')
def end_buy(id):
    session = db_session.create_session()
    sale = session.query(Sale).filter(Sale.id == id).first()
    prod = session.query(Product).filter(Product.id == sale.item).first()

    return render_template('order.html', title='Заказ', ll=geocode.draw_map(prod.address))


@app.route('/create_order/<int:id>')
def buy_product(id):
    prod = session.query(Product).filter(Product.id == id).first().seller
    post('http://localhost:5000/api/sales', json={'seller': current_user.id, 'item': id})
    return redirect(f'/store')


@app.route('/close_order/<int:id>')
def close_order(id):
    put(f'http://localhost:5000/api/sales/{id}')
    return redirect('/profile')


@app.route('/del_sale/<int:id>')
def close_trade(id):
    delete(f'http://localhost:5000/api/sales/{str(id)}')
    return redirect('/profile')


@app.route('/profile')
def view_profile():
    session = db_session.create_session()
    sales = get('http://localhost:5000/api/sales').json()
    lst = list()
    sales_lst = list()
    for i in sales['sales']:
        s = get(f'http://localhost:5000/api/sales/{str(i["id"])}').json()
        if s['sales']['seller'] == current_user.id:
            id = s['sales']['id']
            name = get(f'http://localhost:5000/api/products/{str(id)}').json()['products']['name']
            sold_status = s['sales']['sold_status']
            sales_lst.append([id, name, sold_status])
    return render_template('profile.html', title='Профиль', sales_lst=sales_lst)


def main():
    app.register_blueprint(sales_api.blueprint)
    app.register_blueprint(products_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
