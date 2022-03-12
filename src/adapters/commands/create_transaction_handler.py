from src.models import Node


class CreateTransactionHandler:

    def __init__(self, node: Node) -> None:
        self.node = node

    def handle(self, receiver_address: str, amount: int):
        self.node.create_transaction(receiver_address, amount)
