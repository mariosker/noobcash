from src.repository.ring import RingNode
from src.usecases.block_usecase import BlockUsecase
from src.usecases.bootstrap_node_usecase import BootstrapNodeUsecase
from src.usecases.chain_usecase import ChainUsecase
from src.usecases.node_usecase import NodeUsecase
from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase


class Adapters:

    def __init__(self, is_bootstrap: bool = False, node_count: int = 0):
        self.n_usecase = BootstrapNodeUsecase(
        ) if is_bootstrap else NodeUsecase()

    def create_transaction(self, receiver_address: str, amount: int):
        transaction = TransactionUsecase(self.n_usecase.node)
        transaction.create(receiver_address, amount)

    def get_transactions_from_last_block(self):
        transaction = TransactionUsecase(self.n_usecase.node)
        transaction.get_from_last_block()

    def get_balance(self):
        w_usecase = WalletUsecase(self.n_usecase.node)
        return w_usecase.get_balance()

    def validate_transaction(self):
        transaction = TransactionUsecase(self.n_usecase.node)
        transaction.validate()

    def get_chain(self):
        chain = ChainUsecase(self.n_usecase.node)
        chain.get()

    def register_node(self, node_info: RingNode):
        return self.n_usecase.register(node_info)

    def create_block(self):
        block = BlockUsecase(self.n_usecase.node)
        block.create()

    def set_ring(self, ring):
        self.n_usecase.set_ring(ring)

    def set_blockchain(self, blockchain):
        self.n_usecase.set_blockchain(blockchain)

    def broadcast_ring(self):
        return self.n_usecase.broadcast_ring()
