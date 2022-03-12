from src.models import Node


class GetBalanceHandler:

    def __init__(self, node: Node) -> None:
        self.wallet = node.wallet

    def handle(self) -> int:
        return self.wallet.wallet_balance()
