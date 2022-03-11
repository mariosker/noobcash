from Transaction import Transaction, TransactionOutput
from collections import deque
import crypto


class Wallet:

    def __init__(self) -> None:
        self._private_key, self.public_key = crypto.get_keypair()
        self.transactions = []
        self.unspent_transactions = deque()

    def wallet_balance(self):
        # The balance of the wallet equals the sum of the UTXOs that
        # have as recipient the current wallet.

        balance = 0
        for utxo in self.unspent_transactions:
            balance += utxo.value

        return balance