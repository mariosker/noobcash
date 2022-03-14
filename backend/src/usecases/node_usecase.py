from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node import Node
from src.repository.transaction import Transaction


class NodeUsecase():

    def __init__(self):
        self.node = Node()

    def set_chain(self, blockchain: Blockchain):
        self.node.set_blockchain(blockchain)

    def register_transaction(self, transaction: Transaction):
        self.node.register_transaction(transaction)

    def register_incoming_block(self, block: Block):
        self.node.register_incoming_block(block)
