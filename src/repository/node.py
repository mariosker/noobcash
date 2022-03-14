import pickle
import queue
from collections import deque
from readline import append_history_file
from threading import Thread
from turtle import update

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

    def __init__(self) -> None:
        self.wallet = Wallet()
        self.ring = Ring()
        self.blocks_to_mine = deque()
        self.blockchain = Blockchain()
        self.node_info = RingNode(id=-1,
                                  host=config.HOST,
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  balance=self.wallet.get_balance())
        self.pending_transactions = deque()

        Thread(target=self.handle_pending_transactions).start()

    def broadcast(self, URL: str, obj):
        # TODO: maybe add threading
        responses = []
        for node in self.ring:
            if node == self.node_info:
                continue
            responses.append(
                requests.post(node.host + ':' + node.port + URL, data=obj))

        return responses

    def _broadcast_ring(self):
        data = {'ring': self.ring, 'blockchain': self.blockchain}
        data_pickled = pickle.dumps(data)
        self.broadcast(config.NODE_SET_INFO_URL, data_pickled)

    def create_transaction(self, receiver_address, amount):
        transaction_inputs = []
        transactions_to_be_spent = deque()
        input_amount = 0

        if self.wallet.get_balance() < amount:
            raise ValueError(
                f'You have {self.wallet.get_balance()} coins but want to use {amount} coins'
            )

        while input_amount < amount:
            current_utxo = self.wallet.unspent_transactions.pop()
            transactions_to_be_spent.append(current_utxo)
            input_amount += current_utxo.value
            transaction_inputs.append(
                TransactionInput(current_utxo.id, current_utxo.value))

        transaction = Transaction(self.wallet.public_key, receiver_address,
                                  amount, transaction_inputs,
                                  self.wallet.private_key)

        if not self.validate_transaction(transaction):
            self.wallet.unspent_transactions.extend(transactions_to_be_spent)
            raise ValueError('Transaction is invalid')

        transaction_pickled = pickle.dumps(transaction)
        self.broadcast(config.TRANSACTION_URL, transaction_pickled)
        self.pending_transactions.append(transaction)

    def register_transaction(self, transaction: Transaction):
        """Register a transaction that came from other nodes and queue it to be added in a block

        Args:
            transaction (Transaction): _description_

        Raises:
            ValueError: _description_
        """
        if not self.validate_transaction(transaction):
            raise ValueError('Transaction not valid')

        self.pending_transactions.append(transaction)

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

    # def resolve_conflict(self):
    #     # TODO: implement chains
    #     chains = list()
    #     chains.sort(key=lambda x: len(x), reverse=True)
    #     try:
    #         selected_chain = next(
    #             c for c in chains
    #             if c >= len(self.blockchain.chain) and c.validate_chain())
    #     except StopIteration:
    #         # No such chain handles this
    #         pass

    def mine_block(self, block: Block):
        """Mines the block until it begins with MINING_DIFFICULTY zeroes
        """
        while not block.current_hash.startswith('0' * config.MINING_DIFFICULTY):
            block.nonce += 1
            block.current_hash = block.calculate_hash()

    def set_blockchain(self, blockchain: Blockchain) -> None:
        self.blockchain = blockchain

    def handle_pending_transactions(self):
        while True:
            if len(self.pending_transactions) < config.BLOCK_CAPACITY:
                continue

            transactions = [
                self.pending_transactions.pop()
                for _ in range(config.BLOCK_CAPACITY)
            ]

            pending_block = Block(len(self.blockchain),
                                  Blockchain.get_last_block().current_hash,
                                  transactions)

            self.mine_block(pending_block)

            self._broadcast_block(pending_block)

            try:
                self.register_block(pending_block)
            except ValueError:
                self.pending_transactions.extendleft(transactions)

    def update_transactions(self, block: Block):
        for transaction in block.transactions:
            try:
                self.wallet.update_wallet(transaction)
            except:
                pass
            self.ring.update_balance(transaction)

    def register_block(self, block: Block):
        self.blockchain.add_block(block)
        self.update_transactions(block)

    def _broadcast_block(self, block: Block):
        data_pickled = pickle.dumps(block)
        self.broadcast(config.BLOCK_REGISTER_URL, data_pickled)