from src.repository import Node


class WalletUsecase:

    def __init__(self, node: Node) -> None:
        self.wallet = node.wallet

    def get_balance(self) -> int:
        return self.wallet.wallet_balance()
