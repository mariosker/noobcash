from src.repository import node


class ChainUsecase:

    def __init__(self, node: node) -> None:
        self.node = node

    def get_chain(self):
        return self.node.blockchain.get_chain()
