from __future__ import annotations

import time
import uuid

from src.pkg import crypto


class TransactionDerivative:
    """Mother class of Transaction Inputs and Outputs that helps comparing them
    """

    def __init__(self, id, value):
        self.value = value
        self.id = id

    def __eq__(self, other):
        return self.id == other.id


class TransactionOutput(TransactionDerivative):
    """ Output object in the transaction outputs list
    """

    def __init__(self, transaction_id, receiver, value):
        super().__init__(uuid.uuid4().int, value)
        self.transaction_id = transaction_id
        self.receiver = receiver


class TransactionInput(TransactionDerivative):
    """ Input object in the transaction outputs list
    """

    def __init__(self, id, value):
        super().__init__(id, value)


class Transaction:
    """Transaction that goes in the block
    """

    def __init__(self, sender_address: bytes, receiver_address: bytes,
                 amount: int, transaction_inputs: list[TransactionInput],
                 private_key: bytes) -> None:
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.transaction_inputs = transaction_inputs
        self.timestamp = time.time()
        self.transaction_id = self.calculate_hash()
        self.transaction_outputs = self.get_transaction_outputs()
        self.signature = self.sign_transaction(private_key)

    def calculate_hash(self):
        """Calculates the hash of the transaction

        Returns:
            str: the hash as a string
        """
        to_hash = str(self.sender_address) + str(self.receiver_address) + str(
            self.amount) + str(self.timestamp) + "".join(
                str(vars(t)) for t in self.transaction_inputs)
        return crypto.hash_to_str(to_hash)

    def sign_transaction(self, private_key: bytes):
        """Signs the transaction

        Args:
            private_key (rsa.RSAPrivateKey): The private key of the wallet

        Returns:
            Bytes: The signature
        """
        return crypto.get_signature(self.transaction_id, private_key)

    def verify_signature(self, public_key):
        """Given a public key verifies that a signature is correct

        Args:
            public_key (rsa.RSAPublicKey): The public key of the wallet

        Returns:
            bool: True if signature is valid
        """
        return crypto.is_signature_valid(self.signature, self.transaction_id,
                                         public_key)

    def get_transaction_outputs(self):
        """Generates the outputs of the transaction

        One output is for the receiver(amount of coins to receive) and one for the sender(change from the inputs)

        Returns:
            list(TransactionOutput): list of the two outputs
        """
        total_input_amount = sum(
            input.value for input in self.transaction_inputs)

        sender_output = TransactionOutput(transaction_id=self.transaction_id,
                                          receiver=self.sender_address,
                                          value=total_input_amount -
                                          self.amount)

        receiver_output = TransactionOutput(transaction_id=self.transaction_id,
                                            receiver=self.receiver_address,
                                            value=self.amount)

        return [sender_output, receiver_output]

    def __lt__(self, other: Transaction):
        """Check if object Transaction is less than another Transaction object

        Args:
            other (Transaction): The Transaction object to be compared to


        Returns:
            Bool: Return true if this transaction was created before the other
        """
        return self.timestamp < other.timestamp

    def __eq__(self, other: Transaction):
        """Check if two transactions are the same based on their id

        Args:
            other (Transaction): The transaction to be compared to

        Returns:
            Bool: True if they have the same id
        """
        if isinstance(other, self.__class__):
            return self.transaction_id == other.transaction_id
        else:
            return False
