from src.repository.node.node import Node


class WalletUsecase:

    def __init__(self, node: Node) -> None:
        self.wallet = node.wallet

    def get_balance(self) -> int:
        return self.wallet.get_balance()
