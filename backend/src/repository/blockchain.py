from __future__ import annotations

from typing import List

from config import config
from src.repository.block import Block


class Blockchain:
    """ Contains the blocks of the blockchain
    """

    def __init__(self, chain: List[Block] = None) -> None:
        self.chain = chain

    def add_block(self, block: Block):
        """Adds a block to the chain

        Args:
            block (Block): the block to be added

        Raises:
            ValueError: Block is not valid
        """
        if self.validate_block(block):
            self.chain.append(block)
        else:
            raise ValueError("Block is not valid")

    def validate_block(self, block: Block) -> bool:
        """Checks if the block is valid

        Args:
            block (Block): A block instance to check if it is valid

        Returns:
            bool: True if valid else False
        """
        prev_block = self.chain[block.index - 1]

        has_valid_hash = (block.current_hash == block.calculate_hash())
        points_to_prev_block = (block.previous_hash == prev_block.current_hash)

        return has_valid_hash and points_to_prev_block

    def validate_chain(self) -> bool:
        """checks if all blocks are valid

        Returns:
            bool: True if chain is valid
        """
        if all(self.validate_block(block) for block in self.chain[1:]):
            return True
        return False

    def __len__(self):
        """length of the blockchain

        Returns:
            int: length of the blockchain object
        """
        return len(self.chain)

    def get_last_block(self) -> Block:
        """Returns the last block of the blockchain

        Returns:
            block (Block): A block instance
        """
        if not self.chain:
            return None
        return self.chain[-1]

    def get_chain(self) -> List[Block]:
        """Returns a chain of Blocks

        Returns:
            List[Block]: A list of all the blocks in the blockchain
        """
        return self.chain

    def __lt__(self, other: Blockchain):
        """compare the current blockchain with another. Comparison of blockchain length

        Args:
            other (Blockchain): The blockchain to be compaired with

        Returns:
            Bool: True if blockchain less than the other blockchain
        """
        return len(self.chain) < len(other.chain)
