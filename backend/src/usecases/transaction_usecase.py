from src.repository.node.node import Node
from src.repository.transaction import Transaction


class TransactionUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def create(self, node_id: int, amount: int):
        try:
            node = self.node.ring.get_node_by_id((node_id))

            if not node:
                raise ValueError("Not a node")

            self.node.create_transaction(node.public_key,
                                         amount) if node else False
            res = True
        except Exception as err:
            print(err)
            res = False
        return res

    def get_transactions_from_last_block(self):
        last_block = self.node.blockchain.get_last_block()
        if not last_block:
            return []
        transactions = last_block.get_transactions()

        return [vars(t) for t in transactions]

    def register(self, transaction: Transaction):
        return self.node.register_transaction(transaction)
