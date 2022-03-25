from src.repository.node.p2p_node import P2PNode
from src.repository.ring import Ring
from src.usecases.node.node_usecase import NodeUsecase


class P2PNodeUsecase(NodeUsecase):

    def __init__(self):
        super().__init__()
        self.node = P2PNode()

    def set_ring(self, ring: Ring):
        """set the ring of the node

        Args:
            ring (Ring): The ring to update the node's ring
        """
        self.node.set_ring(ring)
