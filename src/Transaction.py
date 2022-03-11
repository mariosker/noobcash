import crypto
from dataclasses import dataclass


@dataclass
class TransactionOutput:
    transaction_id: str
    receiver: str
    value: int
    id: int = crypto.get_random_hash()


class Transaction:

    def __init__(self, sender_address, receiver_address, amount,
                 transaction_inputs, transaction_outputs) -> None:
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.transaction_inputs = transaction_inputs
        self.transaction_outputs = transaction_outputs
        self.transaction_id = self.calculate_hash()
        # self.signature = None

    def calculate_hash(self):
        # TODO: Add more to hash
        to_hash = str(self.sender_address) + str(self.receiver_address) + str(
            self.amount)
        return crypto.hash_to_str(to_hash)

    def sign_transaction(self, private_key):
        return crypto.get_signature(self.transaction_id, private_key)

    def verify_signature(self, public_key):
        return crypto.is_signature_valid(self.signature, self.transaction_id,
                                         public_key)

    def get_transaction_outputs(self):
        # computes the 2 outputs of the transaction
        total_input_amount = sum(
            [input['value'] for input in self.transaction_inputs])

        sender_output = TransactionOutput(transaction_id=self.transaction_id,
                                          receiver=self.sender_address,
                                          value=total_input_amount -
                                          self.amount)
        receiver_output = TransactionOutput(transaction_id=self.transaction_id,
                                            receiver=self.receiver_address,
                                            value=self.amount)

        return [sender_output, receiver_output]
