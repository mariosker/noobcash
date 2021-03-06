import concurrent.futures
import inspect
import pickle
import time
from collections import deque
from copy import deepcopy
from threading import Event, Lock, Thread
from time import sleep

import requests
from config import config
from src.metrics.metrics import (block_time, transaction_counter,
                                 last_mined_block_timestamp,
                                 first_transaction_timestamp)
from src.pkg.requests import poll_endpoint
from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.ring import Ring, RingNode
from src.repository.transaction import Transaction, TransactionInput
from src.repository.wallet import Wallet

flag = True


class Node:
    """User using the blockchain
    """

    def __init__(self) -> None:
        self.wallet = Wallet()
        self.ring = Ring([])
        self.blockchain = Blockchain()
        self.node_info = RingNode(id=-1,
                                  host=config.HOST,
                                  port=config.PORT,
                                  public_key=self.wallet.public_key,
                                  utxos=self.wallet.unspent_transactions,
                                  balance=self.wallet.get_balance())
        self.pending_transactions = deque()
        self.pause_transaction_handler = Event()
        self.lock = Lock()
        self.transaction_lock = Lock()
        Thread(target=self.handle_pending_transactions).start()

    def broadcast(self, URL: str, obj, requests_function=requests.post):
        """Broadcast the given object to the given url with the given request function

        Args:
            URL (str): the url to which we want to broadcast
            obj (_type_): the object we want to broadcast
            requests_function (_type_, optional): the function used for the request. Defaults to requests.post.
        """

        def make_request(url):
            if requests_function == requests.post:
                return poll_endpoint(url, request_type='post', data=obj)
            else:
                return poll_endpoint(url, request_type='get', data=obj)

        url_list = [
            f'http://{node.host}:{node.port}{URL}' for node in self.ring
            if node.public_key != self.wallet.public_key
        ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            responses = [executor.submit(make_request, url) for url in url_list]
            concurrent.futures.wait(responses)

        return [r.result() for r in responses]

    def create_transaction(self, receiver_address: bytes, amount: int):
        """Create a transaction of amount noobcash coins to the given receiver address

        Args:
            receiver_address (bytes): the address of the receiver
            amount (int): the amount of noobcash coins

        Raises:
            ValueError: You do not have enough coins to make the transaction
            ValueError: Transaction is invalid
        """
        global flag
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        if calframe[1][3] != "_send_first_transactions" and flag:
            flag = False
            first_transaction_timestamp.set(time.time())

        self.transaction_lock.acquire()
        transaction_inputs = []
        transactions_to_be_spent = deque()
        input_amount = 0
        if self.wallet.get_balance() < amount:
            self.transaction_lock.release()
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
            self.transaction_lock.release()
            raise ValueError('Transaction is invalid')

        if calframe[1][3] != "_send_first_transactions":
            transaction_counter.inc(1)

        self.wallet.update_wallet(transaction)
        self.ring.update_unspent_transactions(transaction)
        self.pending_transactions.append(transaction)

        transaction_pickled = pickle.dumps(transaction)
        Thread(target=self.broadcast,
               args=(config.TRANSACTION_REGISTER_URL,
                     transaction_pickled)).start()

        self.transaction_lock.release()

    def register_transaction(self, transaction: Transaction):
        """Register a transaction that came from other nodes and queue it to be added in a block

        Args:
            transaction (Transaction): the transaction to be registered

        Raises:
            ValueError: Transaction not valid
        """
        if not self.validate_transaction(transaction):
            raise ValueError('Transaction not valid')

        self.update_transactions(transaction)
        self.pending_transactions.append(transaction)
        return True

    def validate_transaction(self, transaction: Transaction):
        """Checks if a transaction is valid

        Args:
            transaction (Transaction): the transaction that we want to check

        Returns:
            bool: True if transaction is valid, else False
        """
        if not transaction.verify_signature(transaction.sender_address):
            # config.logger.debug('cannot verify')
            return False

        for node in self.ring:
            if node.public_key == transaction.sender_address:
                # config.logger.debug('Found node')
                if node.balance >= transaction.amount:
                    return True

        return False

    def mine_block(self, block: Block):
        """Mines the block until it begins with MINING_DIFFICULTY zeroes

        Args:
            block (Block): the block to mine

        Raises:
            Exception: Mining interrupted by event
        """
        start_time = time.time()
        while not block.current_hash.startswith('0' * config.MINING_DIFFICULTY):
            if self.pause_transaction_handler.is_set():
                # config.logger.debug('''
                # |------------------|
                # |  STOPPED MINING  |
                # |------------------|
                # ''')
                raise Exception("Mining interrupted by event")
            block.nonce += 1
            block.current_hash = block.calculate_hash()
        # config.logger.debug('''
        # |------------------|
        # |      MINED       |
        # |------------------|
        # ''')
        last_mined_block_timestamp.set(time.time())
        block_time.observe(time.time() - start_time)

    def set_blockchain(self, blockchain: Blockchain) -> None:
        """Sets the current blockchain to the given blockchain

        Args:
            blockchain (Blockchain): the blockchain we want to set
        """
        self.blockchain = blockchain

    def handle_pending_transactions(self):
        """Checks to see if maximum block capacity is reached, and then creates the block, mines it,
        adds it to the blockchain and broadcasts it to the whole network
        """
        while True:
            sleep(0.1)
            if self.pause_transaction_handler.is_set():
                continue

            self.lock.acquire()
            if len(self.pending_transactions) < config.BLOCK_CAPACITY:
                self.lock.release()
                continue

            transactions = [
                self.pending_transactions.pop()
                for _ in range(config.BLOCK_CAPACITY)
            ]

            pending_block = Block(len(self.blockchain),
                                  self.blockchain.get_last_block().current_hash,
                                  transactions)
            try:
                self.mine_block(pending_block)
                self._register_mined_block(pending_block)
            except:
                self.pending_transactions.extendleft(transactions)
            else:
                Thread(target=self._broadcast_block,
                       args=(deepcopy(pending_block),)).start()
            self.lock.release()

    def update_transactions(self, transaction: Transaction):
        """Update wallet UTXOs and ring

        Args:
            transaction (Transaction): the transaction with which we update the wallet UTXOs and the ring
        """
        try:
            self.wallet.update_wallet(transaction)
        except Exception as err:
            config.logger.debug("")
        self.ring.update_unspent_transactions(transaction)

    def _register_mined_block(self, block: Block):
        """Registers the mined block to the blockchain

        Args:
            block (Block): the mined block we want to add to the blockchain
        """
        self.blockchain.add_block(block)

    def register_incoming_block(self, block: Block):
        """Registers the incoming block to the blockchain and handles the transactions
        in the pending transactions queue

        Args:
            block (Block): the block to add to the blockchain

        Raises:
            ValueError: Block has wrong index
        """
        self.pause_transaction_handler.set()
        self.lock.acquire()

        try:
            if block.index != self.blockchain.get_last_block().index + 1:
                raise ValueError("Block has wrong index")

            self.blockchain.add_block(block)
            for transaction in block.transactions:
                if transaction in self.pending_transactions:
                    self.pending_transactions.remove(transaction)
                else:
                    self.update_transactions(transaction)
        except Exception as err:
            print(err)
            self.resolve_conflict()

        self.lock.release()
        self.pause_transaction_handler.clear()

    def _broadcast_block(self, block: Block):
        """Broadcasts the given block to the whole network

        Args:
            block (Block): the block to be broadcasted to the whole network
        """
        data_pickled = pickle.dumps(block)
        self.broadcast(config.BLOCK_REGISTER_URL, data_pickled)

    def _request_blockchain(self):
        """Requests the blockchain of all the other nodes in the network

        Returns:
            list: list of the responses content
        """
        responses = self.broadcast(config.NODE_BLOCKCHAIN_URL,
                                   None,
                                   requests_function=requests.get)
        return [pickle.loads(r.content) for r in responses]

    def _request_ring_and_transactions_from_node(self, id):
        """Requests ring and pending transactions of the node with the given id

        Args:
            id (str): the id of the node of which we want to get the ring and pending transactions

        Returns:
            response: response with the requested content
        """
        response = None
        for node in self.ring:
            if node.id == id:
                response = poll_endpoint(
                    f'{node.host}:{node.port}{config.NODE_RING_AND_TRANSACTION}',
                    request_type='get',
                )
                response = pickle.loads(response.content)
                break

        return response

    def resolve_conflict(self):
        """Requests the blockchain of all the other nodes, and if we do not have the longest valid blockchain,
        gets the blockchain, ring and pending transactions of the node that has it.
        """
        responses = self._request_blockchain()
        responses.sort(key=lambda x: Blockchain(x['blockchain']), reverse=True)

        max_response = {'blockchain': self.blockchain, 'id': self.node_info.id}

        for resp in responses:
            current_blockchain = Blockchain(resp['blockchain'])
            if not current_blockchain.validate_chain():
                continue

            if current_blockchain > max_response['blockchain']:
                max_response['blockchain'] = deepcopy(current_blockchain)
                max_response['id'] = resp['id']

        if max_response['id'] == self.node_info.id:
            return

        response = self._request_ring_and_transactions_from_node(
            max_response['id'])

        self.blockchain = deepcopy(max_response['blockchain'])
        self.ring = deepcopy(response['ring'])
        self.pending_transactions = deepcopy(response['transactions'])

        for node in self.ring:
            if node.id == self.node_info.id:
                self.wallet.unspent_transactions = deepcopy(node.utxos)
