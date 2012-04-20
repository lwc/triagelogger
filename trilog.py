import tailer
import msgpack
import zmq
import logging
from sys import argv
import json as json

ZMQ_URI = "tcp://triage.99cluster.com:5001"

logging.basicConfig(level=logging.DEBUG)

logging.info('Initialising 0mq on %s' % argv[2])
try:
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
	socket.connect(argv[2])
except Exception, e:
	logging.error('Failed to connect to zmq server, please specify valid URL as second argument. eg: tcp://triage.99cluster.com:5001')
	exit()

logging.info('Initialising msgpack')
packer = msgpack.Packer()

try:
	logging.info('Opening error log %s' % argv[1])
	errfile = open(argv[1])
except Exception, a:
	logging.error('Failed to open log, please specify valid path as first argument')
	exit()

for line in tailer.follow(errfile):
	try:
		err = json.loads(line)
		socket.send(packer.pack(err))
	except Exception, a:
		logging.exception('Failed to process error')

socket.close()
