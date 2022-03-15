import requests
from cli.config import config
from cli.entities.transaction import TransactionRequest


class RestAPI:
    def __init__(self) -> None:
        pass

    def create_transaction(self, host: str, port: str, transaction: TransactionRequest):
        data = {
            'receiver_address': transaction.receiver_address,
            'amount': transaction.amount,
        }
        requests.post('http://' + host + ':' + port + config.TRANSACTION_URL, data=data)

    def view_last_transactions(self, host: str, port: str):
        requests.get('http://' + host + ':' + port + config.TRANSACTION_URL)

    def get_balance(self, host: str, port: str):
        requests.get('http://' + host + ':' + port + config.BALANCE_URL)
