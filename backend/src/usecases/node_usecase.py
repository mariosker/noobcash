import pickle

from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node import _Node
from src.repository.transaction import Transaction


class NodeUsecase():

    def __init__(self):
        self.node = _Node()

    def set_chain(self, blockchain: Blockchain):
        self.node.set_blockchain(blockchain)

    def register_transaction(self, transaction: Transaction):
        self.node.register_transaction(transaction)

    def register_incoming_block(self, block: Block):
        self.node.register_incoming_block(block)

    def get_ring_and_transactions(self):
        ring_and_transactions = {
            'ring': self.node.ring(),
            'transactions': self.node.pending_transactions
        }

        ring_and_transactions_pickled = pickle.dumps(ring_and_transactions)

        return ring_and_transactions_pickled
