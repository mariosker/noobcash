from src.repository import Node


class TransactionUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def create(self, receiver_address: str, amount: int):
        self.node.create_transaction(receiver_address, amount)

    def get_from_last_block(self):
        pass

    def validate(self):
        pass
