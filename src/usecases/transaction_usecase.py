from src.repository import node, transaction


class TransactionUsecase:

    def __init__(self, node: node) -> None:
        self.node = node

    def create(self, receiver_address: str, amount: int):
        self.node.create_transaction(receiver_address, amount)

    def get_transactions_from_last_block(self):
        last_block = self.node.blockchain.get_last_block()
        if not last_block: return []

        transactions = last_block.get_transactions()

        return [vars(t) for t in transactions]

    def register(self):
        self.node.register_transaction()
