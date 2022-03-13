from src.repository.blockchain import Blockchain
from src.repository.node import Node
from src.repository.ring import Ring, RingNode


class NodeUsecase:

    def __init__(self):
        self.node = Node(-1)

    def set_ring(self, ring: Ring):
        self.node.set_ring(ring)

    def set_blockchain(self, blockchain: Blockchain):
        self.node.set_blockchain(blockchain)
