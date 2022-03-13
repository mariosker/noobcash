from src.repository.blockchain import Blockchain
from src.repository.node import Node


class NodeUsecase():

    def __init__(self):
        self.node = Node()

    def set_blockchain(self, blockchain: Blockchain):
        self.node.set_blockchain(blockchain)
