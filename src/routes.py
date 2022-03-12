from flask import request


class RouteHandler:

    def __init__(self, app, adapter) -> None:
        self.app = app
        self.adapter = adapter
        self._init_endpoints()

    def _add_endpoint(self, rule='/', view_func=None, methods=None):
        self.app.add_url_rule(rule, view_func=view_func, methods=methods)

    def _init_endpoints(self):
        add_endpoint = self._add_endpoint
        add_endpoint('/transactions', self.create_transaction, methods=['POST'])
        add_endpoint('/transactions',
                     self.get_transactions_from_last_block,
                     methods=['GET'])
        add_endpoint('/transactions/validate',
                     self.validate_transaction,
                     methods=['GET'])
        add_endpoint('/balance', self.get_balance, methods=['GET'])
        add_endpoint('/node/register', self.register_node, methods=['POST'])
        add_endpoint('/nodes/blockchain', self.get_chain, methods=['GET'])
        add_endpoint('/nodes/block', self.create_block, methods=['POST'])
        add_endpoint('/ring', self.set_ring, methods=['POST'])

    def create_transaction(self):
        receiver_address = request.args.get("receiver_address")
        amount = request.args.get("amount")
        self.adapter.create_transaction(receiver_address, amount)

    def get_transactions_from_last_block(self):
        self.adapter.get_transactions_from_last_block()

    def validate_transaction(self):
        self.adapter.validate_transaction()

    def get_balance(self):
        self.adapter.get_balance()

    def register_node(self):
        self.adapter.register_node()

    def get_chain(self):
        self.adapter.get_chain()

    def create_block(self):
        self.adapter.create_block()

    def set_ring(self):
        self.adapter.set_ring()
