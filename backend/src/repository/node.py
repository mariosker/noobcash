import pickle
from collections import deque
from threading import Thread
from time import sleep

import requests
from config import config
from src.pkg.requests import poll_endpoint
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.ring import Ring, RingNode
from src.repository.transaction import Transaction, TransactionInput
from src.repository.wallet import Wallet


class _Node:
    """User using the blockchain
    """

    def __init__(self) -> None:
        self.wallet = Wallet()
        self.ring = Ring([])
        self.blocks_to_mine = deque()
        self.blockchain = Blockchain()
        self.node_info = RingNode(id=-1,
                                  host=config.HOST,
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  utxos=self.wallet.unspent_transactions,
                                  balance=self.wallet.get_balance())
        self.pending_transactions = deque()
        self.can_mine = True

        Thread(target=self.handle_pending_transactions).start()

    def broadcast(self, URL: str, obj, requests_function=requests.post):
        responses = []
        for node in self.ring:
            if node.host == self.node_info.host:
                continue
            resp = poll_endpoint('http://' + node.host + ':' + node.port + URL,
                                 data=obj,
                                 requests_function=requests_function)
            responses.append(resp)

        return responses

    def create_transaction(self, receiver_address: str, amount: int):
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

        transaction = Transaction(self.wallet.public_key,
                                  bytes(receiver_address), amount,
                                  transaction_inputs, self.wallet.private_key)

        if not self.validate_transaction(transaction):
            self.wallet.unspent_transactions.extend(transactions_to_be_spent)
            raise ValueError('Transaction is invalid')

        transaction_pickled = pickle.dumps(transaction)
        self.broadcast(config.TRANSACTION_REGISTER_URL, transaction_pickled)
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

        self.update_transactions(transaction)
        self.pending_transactions.append(transaction)

    def validate_transaction(self, transaction: Transaction):
        if not transaction.verify_signature():
            return False

        current_node = self.ring.get_node(
            transaction.sender_address.decode('utf-8'))

        if not current_node:
            return False

        if current_node.balance >= transaction.amount:
            return True

        return False

    def mine_block(self, block: Block):
        """Mines the block until it begins with MINING_DIFFICULTY zeroes
        """
        while not block.current_hash.startswith(
                '0' * config.MINING_DIFFICULTY) and self.can_mine:
            block.nonce += 1
            block.current_hash = block.calculate_hash()

    def set_blockchain(self, blockchain: Blockchain) -> None:
        self.blockchain = blockchain

    def handle_pending_transactions(self):
        # TODO: check locks and stuff
        while True:
            if len(self.pending_transactions
                  ) < config.BLOCK_CAPACITY or not self.can_mine:
                continue

            transactions = [
                self.pending_transactions.pop()
                for _ in range(config.BLOCK_CAPACITY)
            ]

            pending_block = Block(len(self.blockchain),
                                  self.blockchain.get_last_block().current_hash,
                                  transactions)

            self.mine_block(pending_block)

            if self.can_mine:
                self._broadcast_block(pending_block)

                try:
                    self._register_mined_block(pending_block)
                except ValueError:
                    self.pending_transactions.extendleft(transactions)
            else:
                self.pending_transactions.extendleft(transactions)

    def update_transactions(self, transaction: Transaction):
        try:
            self.wallet.update_wallet(transaction)
        except Exception as err:
            config.logger.debug(err)
        self.ring.update_balance(transaction)

    def _register_mined_block(self, block: Block):
        self.blockchain.add_block(block)

    def register_incoming_block(self, block: Block):
        self.can_mine = False
        sleep(3)
        try:
            self.blockchain.add_block(block)

            for transaction in block.transactions:
                if transaction in self.pending_transactions:
                    self.pending_transactions.remove(transaction)
                else:
                    self.update_transactions(transaction)
        except Exception as err:
            config.logger.debug(err)
            self.resolve_confict()
        self.can_mine = True

    def _broadcast_block(self, block: Block):
        data_pickled = pickle.dumps(block)
        self.broadcast(config.BLOCK_REGISTER_URL, data_pickled)

    def _request_blockhain(self):
        responses = self.broadcast(config.NODE_BLOCKCHAIN_URL,
                                   None,
                                   requests_function=requests.get)
        return [pickle.loads(r.data) for r in responses]

    def _request_ring_and_transactions_from_node(self, id):
        response = None
        for node in self.ring:
            if node.id == id:
                response = requests.get(node.host + ':' + node.port +
                                        config.NODE_RING_AND_TRANSACTION)
                response = pickle.loads(response.data)
                break

        return response

    def resolve_confict(self):
        # NOTE: maybe needs threading
        responses = self._request_blockhain()
        responses.sort(key=lambda x: x['blockchain'], reverse=True)

        max_response = {'blockchain': self.blockchain, 'id': self.node_info.id}

        for resp in responses:
            if not resp['blockchain'].validate_chain():
                continue

            max_response = resp if resp['blockchain'] > max_response[
                'blockchain'] else max_response

        if max_response['id'] == self.node_info.id:
            return

        response = self._request_ring_and_transactions_from_node(
            max_response['id'])

        self.blockchain = max_response['blockchain']
        self.ring = response['ring']
        self.pending_transactions = response['transactions']

        for node in self.ring:
            if node.id == self.node_info.id:
                self.wallet.unspent_transactions = node.utxos
