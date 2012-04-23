import tailer
import msgpack
import zmq
import logging
from sys import argv
import json as json

import config

logging.basicConfig(level=config.LOGGING_LEVEL, format='%(asctime)s %(levelname)s %(message)s')

logging.info('Initialising 0mq on %s' % config.HOST_URL)
try:
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.connect(config.HOST_URL)
except Exception, e:
	logging.error('Failed to connect to zmq server, please specify valid URL in config.py')
	exit()

logging.info('Initialising msgpack')
packer = msgpack.Packer()

try:
	logging.info('Opening error log %s' % config.ERROR_FILE)
	errfile = open(config.ERROR_FILE)
except Exception, a:
	logging.error('Failed to open log, please specify valid path in config.py')
	exit()

for line in tailer.follow(errfile):
	logging.debug('Found line')
	try:
		err = json.loads(line)
		logging.debug('Loaded JSON')
		socket.send(packer.pack(err))
		logging.debug('Sent')
	except Exception, a:
		logging.exception('Failed to process error')

socket.close()
