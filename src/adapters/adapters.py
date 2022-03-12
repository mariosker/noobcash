import re
from src.models.Node import Node
from src.adapters.get_balance_handler import GetBalanceHandler
from src.adapters.create_transaction_handler import CreateTransactionHandler
from src.adapters.get_transactions_from_last_block_handler import GetTransactionsFromLastBlockHandler


class Adapters:

    def __init__(self, is_bootstrap: bool = False, node_count: int = 0):
        if is_bootstrap:
            self.node = Node()
        else:
            self.node = Node(1)

    def create_transaction(self, receiver_address: str, amount: int):
        handler = CreateTransactionHandler(self.node)
        handler.handle(receiver_address, amount)

    def get_balance(self):
        handler = GetBalanceHandler(self.node)
        handler.handle()

    def get_transactions_from_last_block(self):
        handler = GetTransactionsFromLastBlockHandler(self.node)
        handler.handle()
