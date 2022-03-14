from collections import deque

from src.pkg import crypto
from src.repository.block import Block
from src.repository.transaction import Transaction


class Wallet:

    def __init__(self) -> None:
        self.private_key, self.public_key = crypto.get_keypair()
        self.unspent_transactions = deque()

    def get_balance(self) -> int:
        """Get the balance of the wallet

        Returns:
            int: the balance
        """
        return sum(utxo.value for utxo in self.unspent_transactions)

    def update_wallet(self, transaction: Transaction):
        if self.public_key == transaction.receiver_address:
            _, utxo = transaction.transaction_outputs
            self.unspent_transactions.append(utxo)
        else:
            raise ValueError("Wallet is not the receiver in the transaction")
