#!/usr/bin/env python

from gevent.server import StreamServer
from jsonrmc import handle
from argparse import ArgumentParser
from configparser import ConfigParser
import os
from koryto import tree
from repository import Directory, Database

def connection(socket, address):
	print ('New connection from %s:%s' % address)

	stream = socket.makefile()
	for line in stream:
		stream.write(handle(root, line) + '\n')
		stream.flush()

if __name__ == '__main__':
	parser = ArgumentParser(description='Blue Server.')
	parser.add_argument('--host', '-H', default='0.0.0.0')
	parser.add_argument('--port', '-p', default=6000, type=int)
	parser.add_argument('--config', '-c', default='.')
	args = parser.parse_args()

	config = ConfigParser()
	configfile = os.path.join(args.config, 'blue.cfg')
	config.read_file(open(configfile), configfile)

	global root
	root = Directory(config[u"blue"][u"root"])

	for t in config[u"blue"][u"types"].split(','):
		t = t.strip()

		Database.types[t] = tree.load(os.path.join(args.config, t))

	server = StreamServer((args.host, args.port), connection)
	server.serve_forever()
