import os
import logging

logger = logging
if os.getenv('env') == 'DEV':
    logger.basicConfig(level=logging.DEBUG)
else:
    logger.basicConfig(level=logging.WARN)

BLOCK_CAPACITY = os.getenv('BLOCK_CAPACITY', 10)
MINING_DIFFICULTY = os.getenv('MINING_DIFFICULTY', 10)
