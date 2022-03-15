from src.repository.node import _Node


class ChainUsecase:

    def __init__(self, node: _Node) -> None:
        self.node = node

    def get_chain(self):
        return self.node.blockchain.get_chain()
