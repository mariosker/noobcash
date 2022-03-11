from collections import deque
from dataclasses import dataclass
import requests
import config
from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction, TransactionInput, TransactionOutput
from Wallet import Wallet


@dataclass
class RingNode:
    """Contains the data of a node in the ring
    """
    id: str
    ip: str
    port: str
    public_key: str
    balance: str


class Node:
    """User using the blockchain
    """

    def __init__(self, id=0) -> None:
        self.id = id
        if not id:
            self.create_genesis_block()
        self.blockchain = Blockchain()
        self.wallet = Wallet()
        self.current_block = None
        self.ring = []
        self.blocks_to_mine = deque()

    def create_genesis_block(self):
        self.current_block = Block(0, 1)

    def create_block(self):
        # New index and previous hash will be updated in mining.
        self.current_block = Block(None, None)

        return self.current_block

    def create_transaction(self, receiver_address, amount):
        transaction_inputs = []
        transactions_to_be_spent = deque()
        input_amount = 0

        if self.wallet.wallet_balance() < amount:
            raise ValueError(
                f'You have {self.wallet.wallet_balance()} coins but want to use {amount} coins'
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
                           transaction_inputs, self.wallet._private_key)

    def broadcast_transaction(self):
        pass

    def validate_transaction(self, transaction: Transaction):
        if not transaction.verify_signature():
            return False

        current_node = next(
            n for n in self.ring if n.public_key == transaction.sender_address)

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

        selected_chain = next(
            c for c in chains
            if c >= len(self.blockchain.chain) and c.validate_chain())

    def register_node_to_ring(self, id, ip, port, public_key, balance):
        self.ring.append(RingNode(id, ip, port, public_key, balance))

    def mine_block(self, block: Block):
        """Mines the block until it begins with MINING_DIFFICULTY zeroes
        """
        while not block.current_hash.startswith('0' * config.MINING_DIFFICULTY):
            block.nonce += 1
            block.current_hash = block.calculate_hash()
