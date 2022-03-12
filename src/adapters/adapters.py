from src.adapters.commands.create_block_handler import CreateBlockHandler
from src.adapters.commands.create_transaction_handler import \
    CreateTransactionHandler
from src.adapters.commands.register_node_handler import RegisterNodeHandler
from src.adapters.commands.set_ring_handler import SetRingHandler
from src.adapters.queries.get_balance_handler import GetBalanceHandler
from src.adapters.queries.get_chain_handler import GetChainHandler
from src.adapters.queries.get_transactions_from_last_block_handler import \
    GetTransactionsFromLastBlockHandler
from src.adapters.queries.validate_transaction import \
    ValidateTransactionHandler
from src.models.Node import Node


class Adapters:

    def __init__(self, is_bootstrap: bool = False, node_count: int = 0):
        self.node = self._create_bootstrap_node(
        ) if is_bootstrap else self._create_node(self)

    def _create_node(self):
        pass

    def _create_bootstrap_node(self):
        node = Node()

    def create_transaction(self, receiver_address: str, amount: int):
        handler = CreateTransactionHandler(self.node)
        handler.handle(receiver_address, amount)

    def get_transactions_from_last_block(self):
        handler = GetTransactionsFromLastBlockHandler(self.node)
        handler.handle()

    def get_balance(self):
        handler = GetBalanceHandler(self.node)
        return handler.handle()

    def validate_transaction(self):
        handler = ValidateTransactionHandler(self.node)
        handler.handle()

    def get_chain(self):
        handler = GetChainHandler(self.node)
        handler.handle()

    def register_node(self):
        handler = RegisterNodeHandler(self.node)
        handler.handle()

    def create_block(self):
        handler = CreateBlockHandler(self.node)
        handler.handle()

    def set_ring(self):
        handler = SetRingHandler(self.node)
        handler.handle()
