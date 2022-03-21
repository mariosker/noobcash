from prometheus_client import Counter, Histogram

transaction_counter = Counter('transaction_counter', 'The number of transactions that the server handled')
block_time = Histogram('block_latency', 'Time to add a block to the blockchain')
