from src.repository.node.node import Node
from src.repository.transaction import Transaction
from datetime import datetime
import json


class TransactionUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def create(self, node_id: int, amount: int):
        try:
            if node_id == self.node.node_info.id:
                raise ValueError("Cannot create transaction to yourself")

            node = self.node.ring.get_node_by_id((node_id))

            if not node:
                raise ValueError("Not a node")

            self.node.create_transaction(node.public_key,
                                         amount) if node else False
            res = True
        except Exception as err:
            print(err)
            res = False
        return res

    def get_transactions_from_last_block(self):
        last_block = self.node.blockchain.get_last_block()
        if not last_block:
            return []
        transactions = last_block.get_transactions()

        transactions_sendable = []
        for t in transactions:

            if t.sender_address == '0':
                sender_id = 'Genesis'
            else:
                sender = self.node.ring.get_node_by_address(t.sender_address)

                if (sender == None):
                    raise ValueError("Cannot find sender")

                sender_id = sender.id

            receiver = self.node.ring.get_node_by_address(t.receiver_address)

            if (receiver == None):
                raise ValueError("Cannot find receiver")

            receiver_id = receiver.id

            transactions_sendable.append({
                'Sender': sender_id,
                'Receiver': receiver_id,
                'Amount': t.amount,
                'Timestamp': datetime.fromtimestamp(t.timestamp).strftime("%c")
            })

        return json.dumps(transactions_sendable)

    def register(self, transaction: Transaction):
        return self.node.register_transaction(transaction)
