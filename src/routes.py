import pickle

from config import config
from flask import request
from numpy import block


class RouteHandler:

    def __init__(self, app, adapter) -> None:
        self.app = app
        self.adapter = adapter
        self._init_endpoints()

    def _add_endpoint(self, rule='/', view_func=None, methods=None):
        self.app.add_url_rule(rule, view_func=view_func, methods=methods)

    def _init_endpoints(self):
        add_endpoint = self._add_endpoint
        add_endpoint(config.TRANSACTION_URL,
                     self.create_transaction,
                     methods=['POST'])
        add_endpoint(config.TRANSACTION_URL,
                     self.get_transactions_from_last_block,
                     methods=['GET'])
        add_endpoint(config.TRANSACTION_VALIDATE_URL,
                     self.validate_transaction,
                     methods=['GET'])
        add_endpoint(config.BALANCE_URL, self.get_balance, methods=['GET'])
        add_endpoint(config.NODE_REGISTER_URL,
                     self.register_node,
                     methods=['POST'])
        add_endpoint(config.NODE_BLOCKCHAIN_URL,
                     self.get_chain,
                     methods=['GET'])
        add_endpoint(config.NODE_BLOCK_URL,
                     self.create_block, methods=['POST'])
        add_endpoint(config.NODE_SET_INFO_URL, self.set_info, methods=['POST'])

    def create_transaction(self):
        receiver_address = request.args.get("receiver_address")
        amount = request.args.get("amount")
        self.adapter.create_transaction(receiver_address, amount)

    def get_transactions_from_last_block(self):
        self.adapter.get_transactions_from_last_block()

    def validate_transaction(self):
        self.adapter.validate_transaction()

    def get_balance(self):
        return str(self.adapter.get_balance())

    def register_node(self):
        node_info = pickle.loads(request.get_data())
        node_info = self.adapter.register_node(node_info)
        return pickle.dumps(node_info)

    def get_chain(self):
        self.adapter.get_chain()

    def create_block(self):
        self.adapter.create_block()

    def set_info(self):
        data = pickle.loads(request.get_data())
        ring = data['ring']
        blockchain = data['blockchain']
        self.adapter.set_ring(ring)
        self.adapter.set_blockchain(blockchain)
        return ('', 204)
