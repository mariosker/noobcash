from src.repository import Node


class NodeUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def register(self):
        self.node.register_node()
