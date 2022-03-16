from src.repository.block import Block
from src.repository.blockchain import Blockchain
from src.repository.ring import Ring, RingNode
from src.repository.transaction import Transaction
from src.usecases.blockchain_usecase import BlockChainUsecase
from src.usecases.bootstrap_node_usecase import BootstrapNodeUsecase
from src.usecases.node_usecase import NodeUsecase
from src.usecases.p2p_node_usecase import P2PNodeUsecase
from src.usecases.transaction_usecase import TransactionUsecase
from src.usecases.wallet_usecase import WalletUsecase


class Adapters:

    def __init__(self):
        self.node_usecase = NodeUsecase()

    def create_transaction(self, receiver_address: bytes, amount: int):
        return TransactionUsecase(self.node_usecase.node).create(
            receiver_address, amount)

    def register_transaction_to_block(self, transaction: Transaction):
        return TransactionUsecase(self.node_usecase.node).register(transaction)

    def register_incoming_block(self, block: Block):
        return self.node_usecase.register_incoming_block(block)

    def get_transactions_from_last_block(self):
        return TransactionUsecase(
            self.node_usecase.node).get_transactions_from_last_block()

    def get_balance(self):
        return WalletUsecase(self.node_usecase.node).get_balance()

    def get_chain(self):
        return BlockChainUsecase(self.node_usecase.node).get_chain()

    def set_chain(self, blockchain: Blockchain):
        return self.node_usecase.set_chain(blockchain)

    def get_ring_and_transactions(self):
        return self.node_usecase.get_ring_and_transactions()


class P2PAdapters(Adapters):

    def __init__(self) -> None:
        super().__init__()
        self.usecase = P2PNodeUsecase()

    def set_ring(self, ring: Ring):
        self.usecase.set_ring(ring)


class BootstapAdapters(Adapters):

    def __init__(self):
        super().__init__()
        self.usecase = BootstrapNodeUsecase()

    def register_node(self, node_info: RingNode):
        return self.usecase.register_node(node_info)
