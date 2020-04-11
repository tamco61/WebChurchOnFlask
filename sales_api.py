import flask
from data import db_session
from data.sales import Sale

blueprint = flask.Blueprint('sales_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/sales')
def get_sales():
    session = db_session.create_session()
    sales = session.query(Sale).all()
    return flask.jsonify(
        {
            'sales':
                [item.to_dict(only=('id', 'sold_status'))
                 for item in sales]
        }
    )


@blueprint.route('/api/sales/<int:id>',  methods=['GET'])
def get_one_sales(id):
    session = db_session.create_session()
    sales = session.query(Sale).get(id)
    if not sales:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'sales': sales.to_dict(only=('id', 'seller', 'item', 'sold_status', 'modified_date'))
        }
    )


@blueprint.route('/api/sales', methods=['POST'])
def create_sales():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['seller', 'item']):
        return flask.jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    sale = Sale()
    sale.seller = flask.request.json['seller']
    sale.item = flask.request.json['item']
    session.add(sale)
    session.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/sales/<int:id>', methods=['DELETE'])
def delete_sales(id):
    session = db_session.create_session()
    sales = session.query(Sale).get(id)
    if not sales:
        return flask.jsonify({'error': 'Not found'})
    session.delete(sales)
    session.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/sales/<int:id>', methods=['PUT'])
def put_sales(id):
    session = db_session.create_session()
    sales = session.query(Sale).get(id)
    if not sales:
        return flask.jsonify({'error': 'Not found'})
    sales.sold_status = True
    session.commit()
    return flask.jsonify({'success': 'OK'})
