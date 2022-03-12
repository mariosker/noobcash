from flask import Blueprint
import adapters

api = Blueprint('api', __name__, url_prefix='/api/cli')


# create transaction
@api.route('/transactions', method=['POST'])
def create_transaction():
    adapters.create_transaction()


@api.route('/transactions', method=['GET'])
def get_transactions_from_last_block():
    adapters.get_transactions_from_last_block()


@api.route('/balance', method=['GET'])
def get_balance():
    adapters.get_balance()


'''
client:
* create_transaction
* get_balance
* get_transaction_from_last_block

peers:
* validate_transaction
* post_transaction

* post_node

* get_ring
* post_ring

* get_chain
* post_chain

* post_block
'''



class RouteHandler:
    def __init__(self, app, adapter) -> None:
        pass

    def init_endpoints(self):
        pass
