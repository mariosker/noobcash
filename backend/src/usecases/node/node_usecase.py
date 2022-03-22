import pickle

from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node.node import Node
from src.repository.transaction import Transaction


class NodeUsecase():

    def __init__(self):
        # TODO: remove node because it is initialized elsewhere
        self.node = Node()

    def set_chain(self, blockchain: Blockchain):
        self.node.set_blockchain(blockchain)

    def register_incoming_block(self, block: Block):
        self.node.register_incoming_block(block)

    def get_ring_and_transactions(self):
        return {
            'ring': self.node.ring,
            'transactions': self.node.pending_transactions
        }
