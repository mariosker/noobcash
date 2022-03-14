from src.adapters import Adapters
from src.repository.ring import RingNode
from src.usecases.bootstrap_node_usecase import BootstrapNodeUsecase


class BootstapAdapters(Adapters):
    def __init__(self):
        super().__init__()
        self.usecase = BootstrapNodeUsecase()

    def register_node(self, node_info: RingNode):
        return self.usecase.register_node(node_info)
