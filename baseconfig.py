import logging

ERROR_FILE = ''
HOST_URL = '' # eg. tcp://triage.yourserver.com:5001
LOGGING_LEVEL = logging.DEBUG

try:
    from config import *
except ImportError:
    pass

