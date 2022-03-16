import pickle

from config import config
from flask import Flask, request

from src.adapters import Adapters, BootstapAdapters, P2PAdapters


class RouteHandler:

    def __init__(self, app: Flask, adapter: Adapters) -> None:
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
        add_endpoint(config.TRANSACTION_REGISTER_URL,
                     self.register_transaction_to_block,
                     methods=['POST'])
        add_endpoint(config.TRANSACTION_URL,
                     self.get_transactions_from_last_block,
                     methods=['GET'])

        add_endpoint(config.BALANCE_URL, self.get_balance, methods=['GET'])

        add_endpoint(config.BLOCK_REGISTER_URL,
                     self.register_incoming_block,
                     methods=['POST'])

        add_endpoint(config.NODE_BLOCKCHAIN_URL,
                     self.get_chain,
                     methods=['GET'])

        add_endpoint(config.NODE_BLOCKCHAIN_URL,
                     self.set_chain,
                     methods=['POST'])

        add_endpoint(config.NODE_RING_AND_TRANSACTION,
                     self.get_ring_and_transactions,
                     methods=['GET'])

    def create_transaction(self):
        receiver_address = request.args.get("receiver_address")
        amount = request.args.get("amount")
        if self.adapter.create_transaction(receiver_address, amount):
            return ('could not create transaction', 500)
        return ('transaction created successfully', 200)

    def register_transaction_to_block(self):
        transaction = pickle.loads(request.get_data())
        return self.adapter.register_transaction_to_block(transaction)

    def register_incoming_block(self):
        block = pickle.loads(request.get_data())
        return self.adapter.register_incoming_block(block)

    def get_transactions_from_last_block(self):
        return self.adapter.get_transactions_from_last_block()

    def get_balance(self):
        return str(self.adapter.get_balance())

    def get_chain(self):
        self.adapter.get_chain()

    def set_chain(self):
        self.adapter.set_chain()

    def get_ring_and_transactions(self):
        self.adapter.get_ring_and_transactions()


class BootstrapRouteHandler(RouteHandler):

    def __init__(self, app, adapter: BootstapAdapters) -> None:
        super().__init__(app, adapter)
        self._init_specific_endpoints()

    def _init_specific_endpoints(self):
        add_endpoint = self._add_endpoint
        add_endpoint(config.NODE_REGISTER_URL,
                     self.register_node,
                     methods=['POST'])

    def register_node(self):
        node_info = pickle.loads(request.get_data())
        ip = request.environ['REMOTE_ADDR']
        port = str(request.environ['REMOTE_PORT'])
        node_info = self.adapter.register_node(node_info)

        node_info.host = ip
        node_info.port = port
        return pickle.dumps(node_info)


class P2PRouteHandler(RouteHandler):

    def __init__(self, app, adapter: P2PAdapters) -> None:
        super().__init__(app, adapter)
        self._init_specific_endpoints()

    def _init_specific_endpoints(self):
        add_endpoint = self._add_endpoint
        add_endpoint(config.NODE_SET_INFO_URL, self.set_info, methods=['POST'])

    def set_info(self):
        data = pickle.loads(request.get_data())
        ring = data['ring']
        blockchain = data['blockchain']
        self.adapter.set_ring(ring)
        self.adapter.set_chain(blockchain)
        return ('', 204)
