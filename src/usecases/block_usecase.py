from src.repository import block, node


class BlockUsecase:

    def __init__(self, node: node) -> None:
        self.node = node

    def create(self) -> block:
        return self.node.create_block()
