from src.repository import node


class WalletUsecase:

    def __init__(self, node: node) -> None:
        self.wallet = node.wallet

    def get_balance(self) -> int:
        return self.wallet.wallet_balance()
