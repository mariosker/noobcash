from src.repository.node.node import Node
from src.repository.transaction import Transaction
from datetime import datetime
import json
from flask import jsonify


class TransactionUsecase:

    def __init__(self, node: Node) -> None:
        self.node = node

    def create(self, node_id: int, amount: int):
        if node_id == self.node.node_info.id:
            return jsonify({
                'message':
                    'Transaction failed. You cannot create transaction to yourself.'
            }), 500

        node = self.node.ring.get_node_by_id((node_id))

        if not node:
            return jsonify({
                'message':
                    'Transaction failed. Node with given ID does not exist in ring.'
            }), 500

        try:
            self.node.create_transaction(node.public_key, amount)
            return jsonify({'message': 'Ok'}), 204
        except Exception:
            return jsonify({
                'message':
                    'Transaction failed. Not enough coins for the transaction or the signature is invalid.'
            }), 500

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
        """Register the transaction in the blockchain

        Args:
            transaction (Transaction): the transaction to be added
        """
        return self.node.register_transaction(transaction)
