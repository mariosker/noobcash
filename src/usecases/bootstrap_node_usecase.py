from src.repository.node import Node


class BootstrapNodeUsecase:

    def __init__(self):
        self.node = Node(0)
        self.node.init_bootstrap()
