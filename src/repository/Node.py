import pickle
import socket
from collections import deque
from config import config
import requests
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.ring import Ring, RingNode
from src.repository.transaction import Transaction, TransactionInput
from src.repository.wallet import Wallet


class Node:
    """User using the blockchain
    """

    def __init__(
        self,
        uid: int = None,
        ring: Ring = Ring(),
        blockchain: Blockchain = Blockchain()
    ) -> None:

        self.wallet = Wallet()
        self.blockchain = blockchain
        self.ring = ring
        self.current_block = None
        self.blocks_to_mine = deque()
        if uid == 0:
            self.node_info = RingNode(id=uid,
                                  host=socket.gethostname(),
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  balance=self.wallet.get_balance())

            self.ring.append(self.node_info)
            self.create_genesis_block()
        else:
            self.node_info = self.get_node_info_from_bootstrap()

    def get_node_info_from_bootstrap(self) -> RingNode:
        """ As a client request from Bootstrap to return the proper NodeInfo with updated ID

        Raises:
            ConnectionRefusedError: Request denied
        """
        ring_node_serial = pickle.dumps(self.node_info)

        resp = requests.post(config.BOOTSTRAP_HOST + ':' +
                             config.BOOTSTRAP_PORT + config.NODE_REGISTER_URL,
                             data={'node': ring_node_serial})

        if resp.status_code != 200:
            raise ConnectionRefusedError("Cannot get uid from bootstrap")

        return pickle.loads(resp.get_data())

    def register_node(self, node_info: RingNode):
        """ As a bootstrap add the node to the ring and update it's id

        Args:
            node_info (RingNode): _description_

        Returns:
            _type_: _description_
        """
        if len(self.ring) > config.MAX_USER_COUNT:
            raise ValueError('')

        node_info.id = len(self.ring)
        self.ring.append(node_info)

       # broadcast to ring

        return node_info

    def create_genesis_block(self):
        genesis_amount = 100 * config.MAX_USER_COUNT
        genesis_transaction = Transaction('0', self.wallet.public_key,
                                          genesis_amount, None,
                                          self.wallet.private_key)
        self.current_block = Block(0, 1, [genesis_transaction])

    def create_block(self):
        # New index and previous hash will be updated in mining.
        self.current_block = Block(None, None)

        return self.current_block

    def create_transaction(self, receiver_address, amount):
        transaction_inputs = []
        transactions_to_be_spent = deque()
        input_amount = 0

        if self.wallet.get_balance() < amount:
            raise ValueError(
                f'You have {self.wallet.get_balance()} coins but want to use {amount} coins'
            )

        while (input_amount <= amount):
            current_utxo = self.wallet.unspent_transactions.pop()
            transactions_to_be_spent.append(current_utxo)
            input_amount += current_utxo.value
            transaction_inputs.append(
                TransactionInput(current_utxo.id, current_utxo.value))

        # TODO: Fix broadcast transaction
        try:
            self.broadcast_transaction()
        except ...:
            self.wallet.unspent_transactions.extend(transactions_to_be_spent)
            return None

        return Transaction(self.wallet.public_key, receiver_address, amount,
                           transaction_inputs, self.wallet.private_key)

    def broadcast_transaction(self):
        pass

    def validate_transaction(self, transaction: Transaction):
        if not transaction.verify_signature():
            return False

        current_node = self.ring.get_node(
            lambda x: (x.public_key == transaction.sender_address))

        if not current_node:
            return False

        if current_node.balance >= transaction.amount:
            return True

        return False

    def broadcast_block(self):
        pass

    def resolve_conflict(self):
        # TODO: implement chains
        chains = list()
        chains.sort(key=lambda x: len(x), reverse=True)
        try:
            selected_chain = next(
                c for c in chains
                if c >= len(self.blockchain.chain) and c.validate_chain())
        except StopIteration:
            # No such chain handles this
            pass

    def mine_block(self, block: Block):
        """Mines the block until it begins with MINING_DIFFICULTY zeroes
        """
        while not block.current_hash.startswith('0' * config.MINING_DIFFICULTY):
            block.nonce += 1
            block.current_hash = block.calculate_hash()
