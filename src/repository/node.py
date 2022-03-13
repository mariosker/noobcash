import pickle
from collections import deque

import requests
from config import config
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.ring import Ring
from src.repository.transaction import Transaction, TransactionInput
from src.repository.wallet import Wallet


class Node:
    """User using the blockchain
    """

    def __init__(self) -> None:
        self.wallet = Wallet()
        self.ring = Ring()
        self.blocks_to_mine = deque()
        self.blockchain = Blockchain()

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

    def set_blockchain(self, blockchain: Blockchain) -> None:
        self.blockchain = blockchain
