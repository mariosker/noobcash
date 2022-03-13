from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase
from src.usecases.chain_usecase import ChainUsecase
from src.usecases.node_usecase import NodeUsecase
from src.usecases.block_usecase import BlockUsecase
from src.usecases.ring_usecase import RingUsecase
from src.repository.Node import Node


class Adapters:

    def __init__(self, is_bootstrap: bool = False, node_count: int = 0):
        self.node = self._create_bootstrap_node(
        ) if is_bootstrap else self._create_node()

    def _create_node(self):
        pass

    def _create_bootstrap_node(self):
        node = Node()

    def create_transaction(self, receiver_address: str, amount: int):
        transaction = TransactionUsecase(self.node)
        transaction.create(receiver_address, amount)

    def get_transactions_from_last_block(self):
        transaction = TransactionUsecase(self.node)
        transaction.get_from_last_block()

    def get_balance(self):
        wallet = WalletUsecase(self.node)
        return wallet.get_balance()

    def validate_transaction(self):
        transaction = TransactionUsecase(self.node)
        transaction.validate()

    def get_chain(self):
        chain = ChainUsecase(self.node)
        chain.get()

    def register_node(self):
        node = NodeUsecase(self.node)
        node.register()

    def create_block(self):
        block = BlockUsecase(self.node)
        block.create()

    def set_ring(self):
        ring = RingUsecase(self.node)
        ring.set_for_all_nodes()
