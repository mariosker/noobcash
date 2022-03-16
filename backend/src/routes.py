import pickle

from config import config
from flask import Flask, request

from src.usecases.blockchain_usecase import BlockChainUsecase
from src.usecases.bootstrap_node_usecase import BootstrapNodeUsecase
from src.usecases.node_usecase import NodeUsecase
from src.usecases.p2p_node_usecase import P2PNodeUsecase
from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase


class RouteHandler:

    def __init__(self, app: Flask) -> None:
        self.app = app
        self.node_usecase = NodeUsecase()
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
        if TransactionUsecase(self.node_usecase.node).create(
            receiver_address, amount):
            return ('could not create transaction', 500)
        return ('transaction created successfully', 200)

    def register_transaction_to_block(self):
        transaction = pickle.loads(request.get_data())
        return TransactionUsecase(self.node_usecase.node).register(transaction)

    def register_incoming_block(self):
        block = pickle.loads(request.get_data())
        return self.node_usecase.register_incoming_block(block)

    def get_transactions_from_last_block(self):
        return TransactionUsecase(self.node_usecase.node).get_transactions_from_last_block()

    def get_balance(self):
        return str(WalletUsecase(self.node_usecase.node).get_balance())

    def get_chain(self):
        return BlockChainUsecase(self.node_usecase.node).get_chain()

    def set_chain(self):
        chain = pickle.loads(request.get_data())
        return self.node_usecase.set_chain(chain)

    def get_ring_and_transactions(self):
        return self.node_usecase.get_ring_and_transactions()


class BootstrapRouteHandler(RouteHandler):

    def __init__(self, app) -> None:
        super().__init__(app)
        self.usecase = BootstrapNodeUsecase()
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
        node_info = self.usecase.register_node(node_info)
        node_info.host = ip
        node_info.port = port
        return pickle.dumps(node_info)


class P2PRouteHandler(RouteHandler):

    def __init__(self, app) -> None:
        super().__init__(app)
        self.usecase = P2PNodeUsecase()
        self._init_specific_endpoints()

    def _init_specific_endpoints(self):
        add_endpoint = self._add_endpoint
        add_endpoint(config.NODE_SET_INFO_URL, self.set_info, methods=['POST'])

    def set_info(self):
        data = pickle.loads(request.get_data())
        ring = data['ring']
        blockchain = data['blockchain']
        self.usecase.set_ring(ring)
        self.node_usecase.set_chain(blockchain)
        return ('', 204)
