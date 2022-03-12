from src.models import Node


class RegisterNodeHandler:

    def __init__(self, node: Node) -> None:
        self.node = node

    def handle(self):
        self.node.register_node()
