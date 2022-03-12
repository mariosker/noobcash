import os
import logging

logger = logging
if os.getenv('env') == 'DEV':
    logger.basicConfig(level=logging.DEBUG)
else:
    logger.basicConfig(level=logging.WARN)

MAX_USER_COUNT = os.getenv('MAX_USER_COUNT', None)
IS_BOOTSRAP = os.getenv('IS_BOOTSTAP', None)
BLOCK_CAPACITY = os.getenv('BLOCK_CAPACITY', '10')
MINING_DIFFICULTY = os.getenv('MINING_DIFFICULTY', '10')
