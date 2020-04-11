import flask
from data import db_session
from data.products import Product

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/products')
def get_news():
    session = db_session.create_session()
    products = session.query(Product).all()
    return flask.jsonify(
        {
            'products':
                [item.to_dict(only=('id', 'name'))
                 for item in products]
        }
    )


@blueprint.route('/api/products/<int:id>',  methods=['GET'])
def get_one_products(id):
    session = db_session.create_session()
    products = session.query(Product).get(id)
    if not products:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'products': products.to_dict(only=('id', 'name', 'seller', 'price', 'address'))
        }
    )


@blueprint.route('/api/products', methods=['POST'])
def create_products():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['name', 'seller', 'price', 'address']):
        return flask.jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    prod = Product()
    prod.name = flask.request.json['name']
    prod.seller = flask.request.json['seller']
    prod.price = flask.request.json['price']
    prod.address = flask.request.json['address']
    session.add(prod)
    session.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/products/<int:id>', methods=['DELETE'])
def delete_products(id):
    session = db_session.create_session()
    products = session.query(Product).get(id)
    if not products:
        return flask.jsonify({'error': 'Not found'})
    session.delete(products)
    session.commit()
    return flask.jsonify({'success': 'OK'})
