from dataclasses import dataclass


@dataclass
class RingNode:
    """Contains the data of a node in the ring
    """
    id: str
    host: str
    port: str
    public_key: str
    balance: str = 0

    def __eq__(self, other):
        if isinstance(other, RingNode):
            return self.id == other.id
        return False


class Ring:

    def __init__(self, ring: list[RingNode] = []) -> None:
        self.ring = ring

    def append(self, node: RingNode):
        self.ring.append(node)

    def __len__(self):
        return len(self.ring)

    def get_node(self, key):
        try:
            return next(n for n in self.ring if key(n))
        except StopIteration:
            return None

    def __iter__(self):
        for each in self.ring:
            yield each
