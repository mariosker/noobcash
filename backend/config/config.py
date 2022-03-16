import logging
import socket
import os
from sre_constants import IN_IGNORE

logger = logging
if os.getenv('env') != 'PROD':
    logger.basicConfig(level=logging.DEBUG)
else:
    logger.basicConfig(level=logging.WARN)

IGNORE_ARGS = os.getenv("IGNORE_ARGS",
                        'False').lower() in ('true', '1', 't', 'y', 'yes')
IS_LOCAL = True

HOST = os.getenv('HOST', socket.gethostbyname(socket.gethostname()))
PORT = os.getenv('PORT', None)

IS_BOOTSRAP = os.getenv("IS_BOOTSTRAP",
                        'False').lower() in ('true', '1', 't', 'y', 'yes')
BOOTSTRAP_HOST = os.getenv('BOOTSTRAP_HOST', 'localhost')
BOOTSTRAP_PORT = int(os.getenv('BOOTSTRAP_PORT', '5000'))

MAX_USER_COUNT = int(os.getenv('MAX_USER_COUNT', '5'))
BLOCK_CAPACITY = int(os.getenv('BLOCK_CAPACITY', '10'))
MINING_DIFFICULTY = int(os.getenv('MINING_DIFFICULTY', '10'))

NBC_PER_NODE = 100

if IS_BOOTSRAP:
    PORT = BOOTSTRAP_PORT
    BOOTSTRAP_HOST = HOST

TRANSACTION_URL = '/transactions'
TRANSACTION_REGISTER_URL = '/transactions/register'

BALANCE_URL = '/balance'

NODE_REGISTER_URL = '/node/register'
NODE_SET_INFO_URL = '/node/info'
NODE_BLOCKCHAIN_URL = '/node/blockchain'
NODE_RING_AND_TRANSACTION = '/node/ringandtransaction'

BLOCK_REGISTER_URL = '/block/register'
