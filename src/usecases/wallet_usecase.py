from src.repository import node_repository


class WalletUsecase:

    def __init__(self, node: node_repository) -> None:
        self.wallet = node.wallet

    def get_balance(self) -> int:
        return self.wallet.wallet_balance()
