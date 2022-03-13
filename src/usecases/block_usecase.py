from src.repository import Node
from src.repository import Block


class BlockUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def create(self) -> Block:
        return self.node.create_block()
