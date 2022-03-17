import pickle

from src.repository.node.node import Node


class BlockChainUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def get_chain(self):
        chain_and_id = {
            'blockchain': self.node.blockchain.get_chain(),
            'id': self.node.node_info.id
        }

        return chain_and_id
