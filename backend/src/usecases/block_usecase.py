from src.repository.block import Block
from src.repository.node import _Node


class BlockUsecase:

    def __init__(self, node: _Node) -> None:
        self.node = node

    def create(self) -> Block:
        return self.node.create_block()
