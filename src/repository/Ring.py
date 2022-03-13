from dataclasses import dataclass


@dataclass
class RingNode:
    """Contains the data of a node in the ring
    """
    id: str
    host: str
    port: str
    public_key: str
    balance: str


class Ring:

    def __init__(self, ring: list[RingNode] = []) -> None:
        self.ring = ring

    def append(self, node: RingNode):
        self.ring.append(node)

    def get_node(self, key):
        try:
            return next(n for n in self.ring if key(n))
        except StopIteration:
            return None
