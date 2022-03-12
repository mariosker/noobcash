from src.repository import node_repository
from src.repository import Block


class BlockUsecase:

    def __init__(self, node: node_repository) -> None:
        self.node = node

    def create(self) -> Block:
        return self.node.create_block()
