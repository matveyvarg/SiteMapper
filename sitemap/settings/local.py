import logging
from os import getenv

configuration = {
    'host': getenv('HOST', ''),
    'port': getenv('PORT', ''),
    'debug': getenv('DEBUG', True)
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
