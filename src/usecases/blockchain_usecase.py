from src.repository.node import Node


class ChainUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def get_chain(self):
        return self.node.blockchain.get_chain()
