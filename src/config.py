import logging
import os

logger = logging
if os.getenv('env') == 'DEV':
    logger.basicConfig(level=logging.DEBUG)
else:
    logger.basicConfig(level=logging.WARN)

IS_BOOTSRAP = os.getenv('IS_BOOTSTAP', None)
BOOTSTRAP_HOST = os.getenv('BOOTSTRAP_HOST', 'localhost')
BOOTSTRAP_PORT = os.getenv('BOOTSTRAP_PORT', 5000)

MAX_USER_COUNT = os.getenv('MAX_USER_COUNT', None)
BLOCK_CAPACITY = os.getenv('BLOCK_CAPACITY', '10')
MINING_DIFFICULTY = os.getenv('MINING_DIFFICULTY', '10')

PORT = os.getenv('PORT', None)

if IS_BOOTSRAP:
    PORT = BOOTSTRAP_PORT
