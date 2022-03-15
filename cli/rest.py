import json

import requests

from config import config
from entities.transaction import TransactionRequest


class RestAPI:
    def __init__(self) -> None:
        pass

    def create_transaction(self, host: str, port: str, transaction: TransactionRequest) -> json:
        resp = requests.post('http://' + host + ':' + port + config.TRANSACTION_URL, json=transaction.to_json())
        return json.dumps(resp.json())

    def view_last_transactions(self, host: str, port: str):
        resp = requests.get(host + ':' + port + config.TRANSACTION_URL)
        return json.dumps(resp.json())

    def get_balance(self, host: str, port: str):
        resp = requests.get(host + ':' + port + config.BALANCE_URL)
        return json.dumps(resp.json())
