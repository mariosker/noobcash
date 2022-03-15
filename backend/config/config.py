import logging
import os

logger = logging
if os.getenv('env') != 'PROD':
    logger.basicConfig(level=logging.DEBUG)
else:
    logger.basicConfig(level=logging.WARN)

IS_LOCAL = True
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
IS_BOOTSRAP = bool(os.getenv('IS_BOOTSTRAP'))
BOOTSTRAP_HOST = os.getenv('BOOTSTRAP_HOST')
BOOTSTRAP_PORT = os.getenv('BOOTSTRAP_PORT')

MAX_USER_COUNT = int(os.getenv('MAX_USER_COUNT'))
BLOCK_CAPACITY = int(os.getenv('BLOCK_CAPACITY', '10'))
MINING_DIFFICULTY = int(os.getenv('MINING_DIFFICULTY', '10'))


if IS_BOOTSRAP:
    PORT = BOOTSTRAP_PORT

TRANSACTION_URL = '/transactions'
TRANSACTION_REGISTER_URL = '/transactions/register'

BALANCE_URL = '/balance'

NODE_REGISTER_URL = '/node/register'
NODE_SET_INFO_URL = '/node/info'
NODE_BLOCKCHAIN_URL = '/node/blockchain'
NODE_RING_AND_TRANSACTION = '/node/ringandtransaction'

BLOCK_REGISTER_URL = '/block/register'
