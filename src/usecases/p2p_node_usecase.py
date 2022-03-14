from src.repository.blockchain import Blockchain
from src.repository.p2p_node import P2PNode
from src.repository.ring import Ring
from src.usecases.node_usecase import NodeUsecase


class P2PNodeUsecase(NodeUsecase):

    def __init__(self):
        super().__init__()
        self.node = P2PNode()

    def set_ring(self, ring: Ring):
        self.node.set_ring(ring)
