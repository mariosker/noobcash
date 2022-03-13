import pickle
from collections import deque
from threading import Thread

import requests
from config import config
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.ring import Ring, RingNode
from src.repository.transaction import (Transaction, TransactionInput,
                                        TransactionOutput)
from src.repository.wallet import Wallet


class Node:
    """User using the blockchain
    """

    def __init__(self, uid: int = None) -> None:

        self.wallet = Wallet()
        self.ring = Ring()
        self.blocks_to_mine = deque()
        self.blockchain = Blockchain()
        if uid == 0:
            self.node_info = RingNode(id=uid,
                                      host=config.HOST,
                                      port=config.PORT,
                                      public_key=self.wallet.public_key,
                                      balance=self.wallet.get_balance())

            self.ring.append(self.node_info)
            self.current_block = self._create_genesis_block()
            self.blockchain = Blockchain([self.current_block])
        else:
            self.node_info = self._get_node_info_from_bootstrap()

    def _create_genesis_block(self) -> Block:
        genesis_amount = 100 * config.MAX_USER_COUNT
        genesis_transaction = Transaction('0', self.wallet.public_key,
                                          genesis_amount, [],
                                          self.wallet.private_key)
        self.wallet.transactions.append(genesis_transaction)
        [_, receiver_outout] = genesis_transaction.get_transaction_outputs()
        self.wallet.unspent_transactions.append(receiver_outout)
        return Block(0, 1, [genesis_transaction])

    def _get_node_info_from_bootstrap(self) -> RingNode:
        """ As a client request from Bootstrap to return the proper NodeInfo with updated ID

        Raises:
            ConnectionRefusedError: Request denied
        """

        tmp_node_info = RingNode(id=-1,
                                 host=config.HOST,
                                 port=config.PORT,
                                 public_key=self.wallet.public_key)

        ring_node_serial = pickle.dumps(tmp_node_info)

        resp = requests.post(config.BOOTSTRAP_HOST + ':' +
                             config.BOOTSTRAP_PORT + config.NODE_REGISTER_URL,
                             data=ring_node_serial)

        if resp.status_code != 200:
            raise ConnectionRefusedError("Cannot get uid from bootstrap")
        resp_content = pickle.loads(resp.content)
        config.logger.debug(resp_content)
        return resp_content

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
            Thread(target=self._broadcast_ring).start()

        return node_info

    def _broadcast_ring(self):
        data = {'ring': self.ring, 'blockchain': self.blockchain}
        data_pickled = pickle.dumps(data)
        self.broadcast(config.NODE_SET_INFO_URL, data_pickled)

    def create_block(self) -> Block:
        # New index and previous hash will be updated in mining.
        return Block(None, None)

    def create_transaction(self, receiver_address, amount):
        transaction_inputs = []
        transactions_to_be_spent = deque()
        input_amount = 0

        if self.wallet.get_balance() < amount:
            raise ValueError(
                f'You have {self.wallet.get_balance()} coins but want to use {amount} coins'
            )

        while input_amount <= amount:
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

    def broadcast(self, URL: str, obj):
        responses = []
        for node in self.ring:
            if node == self.node_info:
                continue
            responses.append(
                requests.post(node.host + ':' + node.port + URL, data=obj))

        return responses

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

    def set_ring(self, ring: Ring) -> None:
        self.ring = ring

    def set_blockchain(self, blockchain: Blockchain) -> None:
        self.blockchain = blockchain
