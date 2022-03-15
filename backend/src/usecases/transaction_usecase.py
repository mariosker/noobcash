from src.repository.node import _Node
from src.repository.transaction import Transaction


class TransactionUsecase:

    def __init__(self, node: _Node) -> None:
        self.node = node

    def create(self, receiver_address: str, amount: int):
        self.node.create_transaction(receiver_address, amount)

    def get_transactions_from_last_block(self):
        last_block = self.node.blockchain.get_last_block()
        if not last_block:
            return []
        transactions = last_block.get_transactions()

        return [vars(t) for t in transactions]

    def register(self, transaction: Transaction):
        self.node.register_transaction(transaction)
