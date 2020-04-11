import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Sale(SqlAlchemyBase):
    __tablename__ = 'sales'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    seller = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    item = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
    sold_status = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relation('User')
    products = orm.relation('Product')