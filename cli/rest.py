import requests
from config import config
from entities.transaction import TransactionRequest


class RestAPI:

    def __init__(self, host: str, port: str) -> None:
        self.host = 'http://' + host
        self.port = port

    def create_transaction(self, transaction: TransactionRequest):
        data = {
            'receiver_address': transaction.receiver_address,
            'amount': transaction.amount,
        }
        resp = requests.post(self.host + ':' + self.port +
                             config.TRANSACTION_URL,
                             data=data)
        if resp.status_code != 200:
            raise ValueError('cannot create transaction')

    def view_last_transactions(self):
        requests.get(self.host + ':' + self.port + config.TRANSACTION_URL)

    def get_balance(self):
        resp = requests.get(self.host + ':' + self.port + config.BALANCE_URL)
        if resp.status_code != 200:
            raise ValueError('node inaccessible: cannot get balance')