from flask import Flask, render_template, redirect, request, abort
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import PasswordField, TextAreaField, StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from flask_login import current_user, LoginManager, login_user, logout_user, login_required


from data import db_session
from data.users import User

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/database.sqlite")


@app.route('/')
def index():
    return render_template("index.html", title='Главная страница')


def main():
    app.run()


if __name__ == '__main__':
    main()