from src.repository.blockchain import Blockchain
from src.repository.transaction import Transaction
from src.usecases.block_usecase import BlockUsecase
from src.usecases.chain_usecase import ChainUsecase
from src.usecases.node_usecase import NodeUsecase
from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase


class Adapters:

    def __init__(self):
        self.usecase = NodeUsecase()

    def create_transaction(self, receiver_address: str, amount: int):
        transaction = TransactionUsecase(self.usecase.node)
        transaction.create(receiver_address, amount)

    def register_transaction_to_block(self, transaction: Transaction):
        transaction = TransactionUsecase(self.usecase.node)
        transaction.register(transaction)

    def get_transactions_from_last_block(self):
        transaction = TransactionUsecase(self.usecase.node)
        transaction.get_from_last_block()

    def get_balance(self):
        w_usecase = WalletUsecase(self.usecase.node)
        return w_usecase.get_balance()

    def validate_transaction(self):
        transaction = TransactionUsecase(self.usecase.node)
        transaction.validate()

    def get_chain(self):
        chain = ChainUsecase(self.usecase.node)
        chain.get()

    def create_block(self):
        block = BlockUsecase(self.usecase.node)
        block.create()

    def set_blockchain(self, blockchain: Blockchain):
        self.usecase.set_blockchain(blockchain)
