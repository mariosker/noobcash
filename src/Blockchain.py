from Block import Block
from config import logger


class Blockchain:

    def __init__(self, chain: list(Block) = []) -> None:
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
            block (Block): A block instance to be validated

        Returns:
            bool: True if valid else False
        """
        prev_block = self.chain[block.index - 1]
        has_valid_hash = block.current_hash == block.calculate_hash()
        points_to_prev_block = block.previous_hash == prev_block.calculate_hash(
        )

        return has_valid_hash and points_to_prev_block

    def validate_chain(self) -> bool:
        for block in self.chain[1:]:
            if not self.validate_block(block):
                return False
        return True
