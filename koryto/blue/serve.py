#!/usr/bin/env python

from ctypes import CDLL
import gevent.socket as socket
from gevent.server import StreamServer
from jsonrmc import handle
from argparse import ArgumentParser
from koryto.blue.repository import load
import sys
import fdsocket

sd = CDLL("libsystemd-daemon.so")
sd.SD_LISTEN_FDS_START = 3

def connection(socket, address):
	print ('New connection from %s:%s' % (address[0], address[1]))

	stream = socket.makefile()
	for line in stream:
		stream.write(handle(root, line) + '\n')
		stream.flush()

def socketfromfd(fd):
	return socket.fromfd(fd, fdsocket.getfamily(fd), 0)

if __name__ == '__main__':
	parser = ArgumentParser(description='Blue Server.')
	parser.add_argument('--config', '-c', default="{prefix}/etc/koryto/blue")
	args = parser.parse_args()

	global root
	root = load(args.config)

	n = sd.sd_listen_fds(1);

	if n > 1:
		print >> sys.stderr, "Too many file descriptors received."
		exit(1)

	if n < 1:
		print >> sys.stderr, "No file descriptors received."
		exit(1)

	server = StreamServer(socketfromfd(sd.SD_LISTEN_FDS_START), connection)
	server.serve_forever()
