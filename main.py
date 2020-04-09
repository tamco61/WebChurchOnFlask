from flask import Flask, render_template


from data import db_session


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