from koryto.blue.api import Real, Ideal
from koryto.blue.trigger import Trigger

trigger = Trigger()

# BC. TODO: Remove
Object = object
Mixin = object

def launch(args):
	from koryto.blue.repository import load
	from argparse import ArgumentParser

	parser = ArgumentParser(prog = args[0], description='Blue Server.')
	parser.add_argument('--config', '-c', default="{prefix}/etc/koryto/blue")
	args = parser.parse_args(args[1:])

	return load(args.config)
