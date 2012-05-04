import msgpack
import zmq
import logging
import json as json
import subprocess

import baseconfig as config

def tail(filename):
    p = subprocess.Popen(['tail', '-F', '-n', '0', filename],
            stdout=subprocess.PIPE)
    return p.stdout

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

logging.info('Opening error log %s' % config.ERROR_FILE)
for line in tail(config.ERROR_FILE):
	logging.debug('Found line')
	try:
		err = json.loads(line)
		logging.debug('Loaded JSON')
		socket.send(packer.pack(err))
		logging.debug('Sent')
	except Exception, a:
		logging.exception('Failed to process error')

socket.close()
