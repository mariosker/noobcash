from src.repository.node import _Node


class WalletUsecase:

    def __init__(self, node: _Node) -> None:
        self.wallet = node.wallet

    def get_balance(self) -> int:
        return self.wallet.get_balance()
