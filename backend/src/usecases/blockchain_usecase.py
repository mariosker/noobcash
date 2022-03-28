from src.repository.node.node import Node


class BlockChainUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def get_chain(self):
        """Returns the blockchain and the id of the node

        Returns:
            Dict: Dictionary containing the blockchain and id
        """
        chain_and_id = {
            'blockchain': self.node.blockchain.get_chain(),
            'id': self.node.node_info.id
        }

        return chain_and_id
