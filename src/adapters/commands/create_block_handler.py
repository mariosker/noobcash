from src.models import Node
from src.models import Block


class CreateBlockHandler:

    def __init__(self, node: Node) -> None:
        self.node = node

    def handle(self) -> Block:
        return self.node.create_block()
