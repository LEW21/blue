import os
import sys
from configparser import ConfigParser
from koryto import tree
from database import load as loadDB, metabases

class Directory(object):
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

def load(configdir = None):
	if configdir is None:
		configdir = sys.prefix + "/etc/koryto/blue"

	configfile = os.path.join(configdir, 'blue.cfg')
	config = ConfigParser()
	config.read_file(open(configfile), configfile)
	blueconfig = config[u"blue"]

	return Directory(blueconfig[u"root"], metabases([x.strip() for x in blueconfig[u"types"].split(',')], configdir, blueconfig[u"ideals"]))
