import crypto
import uuid


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

    def get_transaction_outputs(self):
        # computes the 2 outputs of the transaction
        balance = sum([input['value'] for input in self.transaction_inputs])

        output1 = {
            'id': uuid.uuid4().int,
            'transaction_id': self.transaction_id,
            'recipient': self.sender_address,
            'value': balance - self.amount
        }
        output2 = {
            'id': uuid.uuid4().int,
            'transaction_id': self.transaction_id,
            'recipient': self.receiver_address,
            'value': self.amount
        }
        return [output1, output2]
