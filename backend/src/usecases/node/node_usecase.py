import pickle

from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node.node import Node
from src.repository.transaction import Transaction


class NodeUsecase():

    def __init__(self):
        self.node = Node()

    def set_chain(self, blockchain: Blockchain):
        self.node.set_blockchain(blockchain)

    def register_incoming_block(self, block: Block):
        self.node.register_incoming_block(block)

    def get_ring_and_transactions(self):
        """Return ring and pending transactions of the node

        Returns:
            Dict(Ring, List[Transaction]): A dict containing the ring and the transactions
        """
        return {
            'ring': self.node.ring(),
            'transactions': self.node.pending_transactions
        }
