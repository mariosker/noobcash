import requests
from config import config


class RestAPI:

    def __init__(self, host: str, port: str) -> None:
        self.host = 'http://' + host
        self.port = port

    def create_transaction(self, receiver, amount):
        data = {'receiver_address': receiver, 'amount': amount}
        resp = requests.post(self.host + ':' + self.port +
                             config.TRANSACTION_URL,
                             data=data)
        if resp.status_code != 200:
            raise ValueError('Cannot create transaction')

        print(f"Transaction successfully created")

    def view_last_transactions(self):
        resp = requests.get(self.host + ':' + self.port +
                            config.TRANSACTION_URL)
        if resp.status_code != 200:
            raise ValueError('Cannot view last transactions')
        return resp.content

    def get_balance(self):
        resp = requests.get(self.host + ':' + self.port + config.BALANCE_URL)
        if resp.status_code != 200:
            raise ValueError('Cannot get balance')
        return int(resp.content)