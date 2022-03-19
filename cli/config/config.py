import logging
import os

logger = logging
if os.getenv('env') != 'PROD':
    logger.basicConfig(level=logging.DEBUG)
else:
    logger.basicConfig(level=logging.WARN)

TRANSACTION_URL = '/transactions'
BALANCE_URL = '/balance'
