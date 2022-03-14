from src.adapters import Adapters
from src.repository.ring import Ring
from src.usecases.p2p_node_usecase import P2PNodeUsecase


class P2PAdapters(Adapters):
    def __init__(self) -> None:
        super().__init__()
        self.usecase = P2PNodeUsecase()

    def set_ring(self, ring: Ring):
        self.usecase.set_ring(ring)
