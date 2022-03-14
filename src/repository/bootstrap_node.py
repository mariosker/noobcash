from threading import Thread

from config import config
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node import Node
from src.repository.ring import RingNode
from src.repository.transaction import Transaction


class BootstrapNode(Node):

    def __init__(self):
        super().__init__()
        self.node_info = RingNode(id=0,
                                  host=config.HOST,
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  balance=self.wallet.get_balance())

        self.ring.append(self.node_info)
        self.current_block = self._create_genesis_block()
        self.blockchain = Blockchain([self.current_block])

    def register_node(self, node_info: RingNode):
        """ As a bootstrap add the node to the ring and update it's id

        Args:
            node_info (RingNode): _description_

        Returns:
            _type_: _description_
        """
        if len(self.ring) > config.MAX_USER_COUNT:
            raise ValueError('Cannot add more nodes to the ring')
        node_info.id = len(self.ring)
        self.ring.append(node_info)
        if len(self.ring) == config.MAX_USER_COUNT:
            # spawn a thread to broadcast the ring to every node.
            Thread(target=self._broadcast_current_state).start()

        return node_info

    def _create_genesis_block(self) -> Block:
        genesis_amount = 100 * config.MAX_USER_COUNT
        genesis_transaction = Transaction('0', self.wallet.public_key,
                                          genesis_amount, [],
                                          self.wallet.private_key)
        self.wallet.transactions.append(genesis_transaction)
        [_, receiver_outout] = genesis_transaction.get_transaction_outputs()
        self.wallet.unspent_transactions.append(receiver_outout)
        return Block(0, 1, [genesis_transaction])
