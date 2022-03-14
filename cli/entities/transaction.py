class TransactionRequest:
    def __init__(self, receiver_address: str, amount: int) -> None:
        self.receiver_address = receiver_address
        self.amount = amount
