import json


class TransactionRequest:
    def __init__(self, receiver_address: str, amount: int) -> None:
        self.receiver_address = receiver_address
        self.amount = amount

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class TransactionResponse:
    def __init__(self, receiver_address: str, amount: int) -> None:
        self.receiver_address = receiver_address
        self.amount = amount

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
