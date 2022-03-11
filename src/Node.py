from Blockchain import Blockchain
from Block import Block
from Wallet import Wallet
from Transaction import Transaction, TransactionOutput


class Node:
    """User using the blockchain
    """

    def __init__(self) -> None:
        self.NBC = 0
        self.chain = Blockchain()
        self.wallet = Wallet()
        self.current_block = None

    def create_block(self):
        if len(self.chain.blocks) == 0:
            # Here, we have only the genesis block.
            self.current_block = Block(0, 1)
        else:
            # New index and previous hash will be updated in mining.
            self.current_block = Block(None, None)

        return self.current_block

    def create_transaction(self, receiver, receiver_id, amount):
        pass

    def broadcast_transaction(self):
        pass

    def validate_transaction(self):
        pass

    def broadcast_block(self):
        pass

    def resolve_conflict(self):
        pass
