import pickle
from threading import Thread

from config import config
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.node import _Node
from src.repository.ring import RingNode
from src.repository.transaction import Transaction


class BootstrapNode(_Node):

    def __init__(self):
        super().__init__()
        self.node_info = RingNode(id=0,
                                  host=config.HOST,
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  utxos=self.wallet.unspent_transactions,
                                  balance=self.wallet.get_balance())

        self.genesis_block = self._create_genesis_block()
        self.ring.append(self.node_info)
        self.blockchain = Blockchain([self.genesis_block])

    def _create_genesis_block(self) -> Block:
        genesis_amount = config.NBC_PER_NODE * config.MAX_USER_COUNT
        genesis_transaction = Transaction('0', self.wallet.public_key,
                                          genesis_amount, [],
                                          self.wallet.private_key)
        [_, receiver_output] = genesis_transaction.transaction_outputs
        self.wallet.unspent_transactions.append(receiver_output)
        self.ring.update_balance(genesis_transaction)
        return Block(0, 1, [genesis_transaction])

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
            Thread(target=self._init_blockchain).start()

        return node_info

    def _init_blockchain(self):
        self._broadcast_current_state()
        self._send_first_transactions()

    def _broadcast_current_state(self):
        data = {'ring': self.ring, 'blockchain': self.blockchain}
        data_pickled = pickle.dumps(data)
        self.broadcast(config.NODE_SET_INFO_URL, data_pickled)

    def _send_first_transactions(self):
        try:
            for node in self.ring:
                if node == self.node_info:
                    continue

                self.create_transaction(node.public_key, config.NBC_PER_NODE)
        except ValueError as err:
            config.logger.debug(err)
            raise ValueError('Could not create initial transactions')
