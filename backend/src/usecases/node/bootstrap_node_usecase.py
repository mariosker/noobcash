from src.repository.node.bootstrap_node import BootstrapNode
from src.repository.ring import RingNode
from src.usecases.node.node_usecase import NodeUsecase


class BootstrapNodeUsecase(NodeUsecase):

    def __init__(self):
        super().__init__()
        self.node = BootstrapNode()

    def register_node(self, node_info: RingNode):
        """Register the node in the Ring

        Args:
            node_info (RingNode): node to be inserted

        Returns:
            RingNode: The updated node
        """
        return self.node.register_node(node_info)
