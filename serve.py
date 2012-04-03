#!/usr/bin/env python
"""Simple server that listens on port 6000 and echos back every input to the client.

Connect to it with:
  telnet localhost 6000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from gevent.server import StreamServer
from jsonrmc import handle
from repository import Directory, Database
from argparse import ArgumentParser

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
	parser.add_argument('root', default='.')
	args = parser.parse_args()

	global root
	root = Directory(args.root)

	server = StreamServer((args.host, args.port), connection)
	server.serve_forever()
