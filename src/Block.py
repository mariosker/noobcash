import time
from hashlib import sha256

import config
from config import logger
import Transaction


class Block:
    """A block for the blockchain
    """

    def __init__(self, index: int, previous_hash: str = "") -> None:
        """_summary_

        Args:
            index (int): the index of the block in the blockchain
            previous_hash (str): hash of the previous block
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = []
        self.nonce = None
        self.previous_hash = previous_hash
        self.current_hash = self.calculate_hash()

    def calculate_hash(self) -> str:

        to_hash = str(self.index) + str(self.timestamp) + str(self.nonce) + str(
            self.previous_hash) + "".join(
                str(t.vars()) for t in self.transactions)
        return sha256(to_hash).hexdigest()

    def add_transaction(self, transaction: Transaction):
        if len(self.transactions < config.BLOCK_CAPACITY):
            self.transactions.append(transaction)
        else:
            raise ValueError(
                f'Block reached capacity of {config.BLOCK_CAPACITY}.')

    def mine_block(self):
        while not self.current_hash.startswith('0' * config.MINING_DIFFICULTY):
            self.nonce += 1
            self.hash = self.calculate_hash()
        logger.debug(f"Block mined with nonce {self.nonce}")
