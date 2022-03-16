from collections import deque
from dataclasses import dataclass
from typing import List

from src.repository.transaction import Transaction


@dataclass
class RingNode:
    """Contains the data of a node in the ring
    """
    id: str
    host: str
    port: str
    public_key: bytes
    utxos: deque()
    balance: int = 0

    def __eq__(self, other):
        if isinstance(other, RingNode):
            return self.id == other.id
        return False


class Ring:

    def __init__(self, ring: List[RingNode] = []) -> None:
        self.ring = ring

    def append(self, node: RingNode):
        """Add a new node to the ring

        Args:
            node (RingNode): A node that contains info about a client in the blockchain
        """
        self.ring.append(node)

    def __len__(self):
        return len(self.ring)

    def get_node(self, sender_address: bytes) -> RingNode:
        """Returns the node with the specific address

        Args:
            sender_address (str): The address of the node to return

        Returns:
            RingNode: A node that contains info about a client in the blockchain
        """
        try:
            return next(n for n in self.ring if sender_address == n.public_key)
        except StopIteration:
            return None

    def __iter__(self):
        for each in self.ring:
            yield each

    def update_balance(self, transaction: Transaction):
        for node in self.ring:
            if node.public_key == transaction.sender_address:
                node.balance -= transaction.amount
                node.utxos = [
                    x for x in node.utxos
                    if x not in transaction.transaction_inputs
                ]

                node.utxos.append(transaction.transaction_outputs[0])

            if node.public_key == transaction.receiver_address:
                node.balance += transaction.amount
                node.utxos.append(transaction.transaction_outputs[1])