from prometheus_client import Counter, Gauge, Histogram

transaction_counter = Counter('transaction_counter', 'The number of transactions that the server handled')
transaction_counter_start = Gauge('transaction_counter_start', 'The timestamp of the first transaction')
transaction_counter_end = Gauge('transaction_counter_end', 'The timestamp of the last transaction')
block_time = Histogram('block_latency', 'Time to add a block to the blockchain')
