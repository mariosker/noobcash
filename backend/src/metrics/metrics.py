from prometheus_client import Counter, Gauge, Histogram

transaction_counter = Counter('transaction_counter', 'The number of transactions that the server handled')
first_transaction_timestamp = Gauge('first_transaction_timestamp', 'The timestamp of the first transaction')
last_mined_block_timestamp = Gauge('last_mined_block_timestamp', 'The timestamp of the last mined block')
block_time = Histogram('block_latency', 'Time to add a block to the blockchain')
