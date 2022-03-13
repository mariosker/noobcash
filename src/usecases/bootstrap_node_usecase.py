from src.repository.bootstrap_node import BootstrapNode
from src.repository.ring import RingNode
from src.usecases.node_usecase import NodeUsecase


class BootstrapNodeUsecase(NodeUsecase):

    def __init__(self):
        super().__init__()
        self.node = BootstrapNode()

    def register(self, node_info: RingNode):
        return self.node.register_node(node_info)
