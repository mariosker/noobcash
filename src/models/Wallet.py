from collections import deque


from src.models.Transaction import Transaction, TransactionOutput
from src.pkg import crypto


class Wallet:

    def __init__(self) -> None:
        self._private_key, self.public_key = crypto.get_keypair()
        self.transactions = []
        self.unspent_transactions = deque()

    def wallet_balance(self) -> int:
        """Get the balance of the wallet

        Returns:
            int: the balance
        """
        balance = sum(utxo.value for utxo in self.unspent_transactions)
        return balance
