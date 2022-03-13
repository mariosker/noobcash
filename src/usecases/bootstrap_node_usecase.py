from src.repository.node import Node
from src.repository.ring import RingNode


class BootstrapNodeUsecase:

    def __init__(self):
        self.node = Node(0)

    def register(self, node_info: RingNode):
        return self.node.register_node(node_info)
