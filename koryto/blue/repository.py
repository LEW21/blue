import os
import sys
from configparser import ConfigParser
from database import load as loadDB, metabases

class Directory(object):
	__slots__ = ["path", "metabases"]

	def __init__(self, path, metabases):
		self.path = path
		self.metabases = metabases

	def __getitem__(self, name):
		path = os.path.join(self.path, name)

		if not os.path.isdir(path):
			raise KeyError

		if os.path.isfile(os.path.join(path, ".db")):
			return loadDB(path, self.metabases)
		else:
			return Directory(path, self.metabases)

def load(configroot = None):
	if configroot is None:
		configroot = "{prefix}/etc/koryto/blue"

	configroot = configroot.format(prefix=sys.prefix)

	config = ConfigParser()

	config.read_dict({"blue": {
		"root": "{prefix}/srv/koryto/blue",
		"ideals": "{prefix}/srv/koryto/ideals",
	}})

	config.read([os.path.join(configroot, 'blue.cfg')])

	blueconfig = config[u"blue"]

	realsroot = blueconfig[u"root"].format(prefix=sys.prefix)
	idealsroot = blueconfig[u"ideals"].format(prefix=sys.prefix)

	try:
		types = [x.strip() for x in blueconfig[u"types"].split(',')]
	except KeyError:
		types = os.listdir(idealsroot)

	return Directory(realsroot, metabases(types, configroot, idealsroot))
