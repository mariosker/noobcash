from collections import deque

from src.pkg import crypto
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
        """Update the wallet's unspent transactions based on a transaction

        Args:
            transaction (Transaction): A transaction object

        Raises:
            ValueError: Error if wallet user is not in the transaction
        """
        if self.public_key == transaction.receiver_address:
            _, utxo = transaction.transaction_outputs
            self.unspent_transactions.append(utxo)
        elif self.public_key == transaction.sender_address:
            utxo, _ = transaction.transaction_outputs
            self.unspent_transactions.append(utxo)
        else:
            raise ValueError("Wallet is not in the transaction")
