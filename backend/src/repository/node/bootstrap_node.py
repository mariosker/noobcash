import pickle
from threading import Thread

from config import config
from copy import deepcopy
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node.node import Node
from src.repository.ring import RingNode
from src.repository.transaction import Transaction


class BootstrapNode(Node):

    def __init__(self):
        super().__init__()
        self.node_info = RingNode(id=0,
                                  host=config.HOST,
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  utxos=deepcopy(
                                      self.wallet.unspent_transactions),
                                  balance=self.wallet.get_balance())

        self.ring.append(self.node_info)
        self.genesis_block = self._create_genesis_block()
        self.blockchain = Blockchain([self.genesis_block])

    def _create_genesis_block(self) -> Block:
        """Create genesis block

        Returns:
            Block: The genesis block
        """
        genesis_amount = config.NBC_PER_NODE * config.MAX_USER_COUNT
        genesis_transaction = Transaction('0', self.wallet.public_key,
                                          genesis_amount, [],
                                          self.wallet.private_key)
        [_, receiver_output] = genesis_transaction.transaction_outputs
        self.wallet.unspent_transactions.append(receiver_output)
        self.ring.update_unspent_transactions(genesis_transaction)
        return Block(0, 1, [genesis_transaction])

    def register_node(self, node_info: RingNode):
        """ Add the node to the ring and update it's id. Then send it

        Args:
            node_info (RingNode): _description_

        Returns:
            RingNode: The update node
        """
        if len(self.ring) > config.MAX_USER_COUNT:
            raise ValueError('Cannot add more nodes to the ring')
        node_info.id = len(self.ring)
        self.ring.append(node_info)

        if len(self.ring) == config.MAX_USER_COUNT:
            Thread(target=self._init_blockchain).start()

        return node_info

    def _init_blockchain(self):
        """after all nodes register start initialization
        """
        self._broadcast_current_state()
        self._send_first_transactions()

    def _broadcast_current_state(self):
        """Broadcasts to all nodes the ring and the blockchain
        """
        data = {'ring': self.ring, 'blockchain': self.blockchain}
        data_pickled = pickle.dumps(data)
        self.broadcast(config.NODE_SET_INFO_URL, data_pickled)

    def _send_first_transactions(self):
        """Once all nodes connect to the noobchain the bootstrap node sends NBC_PER_NODE NBC to them

        Raises:
            ValueError: Error if something bad happens
        """
        try:
            for node in self.ring:
                if node == self.node_info:
                    continue

                self.create_transaction(node.public_key, config.NBC_PER_NODE)
        except ValueError as err:
            # config.logger.debug(err)
            raise ValueError('Could not create initial transactions')
