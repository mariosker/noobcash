import pickle

from config import config
from flask import Flask, request
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.usecases.blockchain_usecase import BlockChainUsecase
from src.usecases.node.bootstrap_node_usecase import BootstrapNodeUsecase
from src.usecases.node.p2p_node_usecase import P2PNodeUsecase
from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase


class RouteHandler:

    def __init__(self, app: Flask) -> None:
        app.wsgi_app = DispatcherMiddleware(app.wsgi_app,
                                            {'/metrics': make_wsgi_app()})
        self.app = app
        self.node_usecase = None

    def _add_endpoint(self, rule='/', view_func=None, methods=None):
        """Adds and endpoint to the apps

        Args:
            rule (str, optional): _description_. Defaults to '/'.
            view_func (_type_, optional): _description_. Defaults to None.
            methods (_type_, optional): _description_. Defaults to None.
        """
        self.app.add_url_rule(rule, view_func=view_func, methods=methods)

    def _init_endpoints(self):
        """Adds endpoints that are crucial to both P2P nodes and Bootstrap Node
        """
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
        """Create a transaction
        """
        node_id = int(request.form['node_id'])
        amount = int(request.form['amount'])
        return TransactionUsecase(self.node_usecase.node).create(
            node_id, amount)

    def register_transaction_to_block(self):
        """Register a transaction in the blockchain

        Returns:
            Response: empty response or error response
        """
        transaction = pickle.loads(request.get_data())
        return ('transaction created successfully', 204) if TransactionUsecase(
            self.node_usecase.node).register(transaction) else (
                'could not create transaction', 500)

    def register_incoming_block(self):
        """Registers a block in the system

        Returns:
            Response: Empty response
        """
        block = pickle.loads(request.get_data())
        self.node_usecase.register_incoming_block(block)
        return ('Block registered', 204)

    def get_transactions_from_last_block(self):
        """Returns the transactions of the last block

        Returns:
            List[Transaction]: the transactions
        """
        return TransactionUsecase(
            self.node_usecase.node).get_transactions_from_last_block()

    def get_balance(self):
        """Returns the balance of the node

        Returns:
            Str: The balance
        """
        return str(WalletUsecase(self.node_usecase.node).get_balance())

    def get_chain(self):
        """Returns the blockchain of the node

        Returns:
            Bytes: the chain pickled
        """
        chain = BlockChainUsecase(self.node_usecase.node).get_chain()
        chain = pickle.dumps(chain)
        return chain

    def set_chain(self):
        """Sets the chain o the node with a given one
        """
        chain = pickle.loads(request.get_data())
        return self.node_usecase.set_chain(chain)

    def get_ring_and_transactions(self):
        """Returns the ring and the transactions of the node

        Returns:
            Bytes: The response pickled
        """
        ring_and_transactions_pickled = pickle.dumps(
            self.node_usecase.get_ring_and_transactions())
        return ring_and_transactions_pickled


class BootstrapRouteHandler(RouteHandler):

    def __init__(self, app) -> None:
        super().__init__(app)
        self.node_usecase = BootstrapNodeUsecase()
        self._init_specific_endpoints()
        self._init_endpoints()

    def _init_specific_endpoints(self):
        """Initializes endpoints of the bootstrap node
        """
        add_endpoint = self._add_endpoint
        add_endpoint(config.NODE_REGISTER_URL,
                     self.register_node,
                     methods=['POST'])

    def register_node(self):
        """Register the node in the blockchain

        Returns:
            NodeRing: The node with updated information
        """
        node_info = pickle.loads(request.get_data())
        node_info = self.node_usecase.register_node(node_info)
        return pickle.dumps(node_info)


class P2PRouteHandler(RouteHandler):

    def __init__(self, app) -> None:
        super().__init__(app)
        self.node_usecase = P2PNodeUsecase()
        self._init_specific_endpoints()
        self._init_endpoints()

    def _init_specific_endpoints(self):
        """Initializes endpoints of the P2P node
        """
        add_endpoint = self._add_endpoint
        add_endpoint(config.NODE_SET_INFO_URL, self.set_info, methods=['POST'])

    def set_info(self):
        """Sets the ring and the blockchain with these given

        Returns:
            Str: empty response
        """
        data = pickle.loads(request.get_data())
        ring = data['ring']
        blockchain = data['blockchain']
        self.node_usecase.set_ring(ring)
        self.node_usecase.set_chain(blockchain)
        return ('', 204)
