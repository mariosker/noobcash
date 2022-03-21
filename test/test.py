import argparse
import concurrent.futures
import json
import os
import random
import time
from concurrent.futures import thread
from functools import partial
from threading import Thread

import requests

random.seed(42)

LIMIT_TRANSACTIONS = None
path = os.getcwd()
node_data = lambda host, port: {'host': host, 'port': port}
nodes = [node_data('http://localhost', p) for p in range(5000, 5005)]


def request_transactions(node, nodes_count):
    host = nodes[node]['host']
    port = nodes[node]['port']
    with open(f"{path}/transactions/{nodes_count}nodes/transactions{node}.txt",
              'r') as f:
        for line in f:
            id_text, amount = line.split(" ")
            id = int(id_text[-1])
            amount = int(amount)

            data = {'node_id': id, 'amount': amount}
            print(node, data)
            requests.post(f'{host}:{port}/transactions', data=data)
            # time.sleep(random.random() * 10)

def get_metrics_output(nodes_count):
    for node in range(nodes_count):
        host = nodes[node]['host']
        port = nodes[node]['port']
        resp = requests.get(f'{host}:{port}/metrics')
        data = resp.content.decode().split('\n')
        for line in data:
            # script kid cause prometheus sucks ¯\_(ツ)_/¯
            if 'block_latency_sum' in line:
                print("id:", node)
                print("Mean time to add a new block to the blockchain:", line.split(' ')[1])
            if '#' not in line and 'transaction_counter_total' in line:
                print("id:", node)
                print("Total transactions made:", line.split(' ')[1])

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
    get_metrics_output(nodes_count)

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
