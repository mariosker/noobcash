from src.repository.node import Node


class NodeUsecase:

    def __init__(self, uid):
        self.node = Node(uid)
