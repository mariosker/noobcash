import requests
from config import config
import json


class RestAPI:

    def __init__(self, host: str, port: str) -> None:
        self.host = 'http://' + host
        self.port = port

    def create_transaction(self, receiver, amount):
        data = {'node_id': receiver, 'amount': amount}
        resp = requests.post(self.host + ':' + self.port +
                             config.TRANSACTION_URL,
                             data=data)
        if resp.status_code == 204:
            print(
                f'Transaction of {amount} NBC coins to node {receiver} successfully created!'
            )
        elif resp.status_code == 500:
            print(resp.json()['message'])
        else:
            print("Transaction failed.")

    def view_last_transactions(self):
        resp = requests.get(self.host + ':' + self.port +
                            config.TRANSACTION_URL)

        if not resp.ok:
            raise ValueError('Cannot view last transactions.')
        return json.loads(resp.content)

    def get_balance(self):
        resp = requests.get(self.host + ':' + self.port + config.BALANCE_URL)
        if not resp.ok:
            raise ValueError('Cannot get balance.')
        return int(resp.content)
