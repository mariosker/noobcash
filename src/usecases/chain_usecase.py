from src.repository import node


class ChainUsecase:

    def __init__(self, node: node) -> None:
        self.node = node

    def get(self):
        pass
