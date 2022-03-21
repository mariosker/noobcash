import argparse
from concurrent.futures import thread
import os
import random
from threading import Thread
import time
import requests
import concurrent.futures
from functools import partial

LIMIT_TRANSACTIONS = None

random.seed(42)

node_data = lambda host, port: {'host': host, 'port': port}
nodes = [node_data('http://localhost', p) for p in range(5000, 5005)]


def request_transactions(node, nodes_count):
    host = nodes[node]['host']
    port = nodes[node]['port']
    with open(f"./transactions/{nodes_count}nodes/transactions{node}.txt",
              'r') as f:
        for line in f:
            id_text, amount = line.split(" ")
            id = int(id_text[-1])
            amount = int(amount)

            data = {'node_id': id, 'amount': amount}
            print(node, data)
            requests.post(f'{host}:{port}/transactions', data=data)
            time.sleep(random.random() * 10)


def main(nodes_count=5):
    threads = []
    for i in range(nodes_count):
        threads.append(
            Thread(target=request_transactions, args=(
                i,
                nodes_count,
            )))

    for i in range(nodes_count):
        threads[i].start()
    for i in range(nodes_count):
        threads[i].join()


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
