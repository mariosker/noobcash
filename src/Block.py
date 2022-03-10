import time

import config
import crypto
from config import logger


class Block:
    """A block of the blockchain
    """

    def __init__(self, index: int, previous_hash: str = "") -> None:
        """Generate a new block.

        Args:
            index (int): the index of the block in the blockchain
            previous_hash (str): hash of the previous block
        """
        self.index = index
        self.timestamp = time.time()
        self.transactions = []
        self.nonce = 0
        self.previous_hash = previous_hash
        self.current_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculates the hash of the block

        Returns:
            str: A hex digest of the hash
        """
        to_hash = str(self.timestamp) + str(self.nonce) + str(
            self.previous_hash) + "".join(
                str(t.vars()) for t in self.transactions)
        return crypto.hash_to_str(to_hash)

    def add_transaction(self, transaction):
        """Adds a transaction to the block

        Args:
            transaction (Transaction): The transaction to be added

        Raises:
            ValueError: Error if block is full
        """
        if len(self.transactions) < config.BLOCK_CAPACITY:
            self.transactions.append(transaction)
        else:
            raise ValueError(
                f'Block reached capacity of {config.BLOCK_CAPACITY}.')

    def mine_block(self):
        """Mines the block until it begins with MINING_DIFFICULTY zeroes
        """
        while not self.current_hash.startswith('0' * config.MINING_DIFFICULTY):
            self.nonce += 1
            self.current_hash = self.calculate_hash()
        logger.debug(f"Block mined with nonce {self.nonce}")
