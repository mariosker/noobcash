import argparse
import os
import random
from threading import Thread
import time
import requests
import concurrent.futures
from functools import partial

LIMIT_TRANSACTIONS = None
node_data = lambda host, port: {'host': host, 'port': port}
nodes = [node_data('localhost', p) for p in range(5000, 5004)]


def request_transactions(node, nodes_count):
    host = nodes[node]['host']
    port = nodes[node]['port']
    count = 0
    with open(f"transactions/{nodes_count}nodes/transactions{node}.txt",
              'r') as f:
        try:
            for line in f:
                count += 1
                id_text, amount = line.split(" ")
                id = int(id_text[-1])
                amount = int(amount)

                data = {'node_id': id, 'amount': amount}
                requests.post(f'{host}:{port}/transactions', params=data)
                time.sleep(random.random() * 5)
                if LIMIT_TRANSACTIONS and count > LIMIT_TRANSACTIONS:
                    break
        except Exception as err:
            print(err)


def main(nodes_count=5):
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=nodes_count) as executor:
        executor.map(partial(request_transactions, nodes_count=nodes_count),
                     range(nodes_count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Noobcash backend')

    parser.add_argument('-n',
                        '--nodes',
                        type=int,
                        default=5,
                        help='The number of nodes in the Noobcash system.')

    args = parser.parse_args()
    nodes_count = int(args.nodes)
    main(nodes_count)
