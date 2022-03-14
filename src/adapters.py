from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.transaction import Transaction
from src.usecases.block_usecase import BlockUsecase
from src.usecases.blockchain_usecase import ChainUsecase
from src.usecases.node_usecase import NodeUsecase
from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase


class Adapters:

    def __init__(self):
        self.node_usecase = NodeUsecase()

    def create_transaction(self, receiver_address: str, amount: int):
        return TransactionUsecase(self.node_usecase.node).create(
            receiver_address, amount)

    def register_transaction_to_block(self, transaction: Transaction):
        return TransactionUsecase(self.node_usecase.node).register(transaction)

    def register_incoming_block(self, block: Block):
        return self.node_usecase.register_incoming_block(block)

    def get_transactions_from_last_block(self):
        return TransactionUsecase(self.node_usecase.node).get_transactions_from_last_block()

    def get_balance(self):
        return WalletUsecase(self.node_usecase.node).get_balance()

    def validate_transaction(self):
        return TransactionUsecase(self.node_usecase.node).validate()

    def get_chain(self):
        return ChainUsecase(self.node_usecase.node).get_chain()

    def set_blockchain(self, blockchain: Blockchain):
        return self.node_usecase.set_blockchain(blockchain)
