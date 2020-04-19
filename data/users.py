import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import jwt
from time import time
from sys import getdefaultencoding

getdefaultencoding()


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    confirm_email = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    privileges = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    products = orm.relation("Product", back_populates='user')
    sales = orm.relation("Sale", back_populates='user')

    def __repr__(self):
        return f"User id: {self.id}, name: {self.name + ' ' + self.surname}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def send_token(self, expires_in=86400):
        return jwt.encode(
            {'user_id': self.id, 'exp': time() + expires_in},
            'secret-key', algorithm='HS256').decode(encoding='UTF-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, 'secret-key',
                            algorithms=['HS256'])['user_id']
        except:
            return
        return id
