import os
import sys
import local
import json
from configparser import ConfigParser
from koryto import tree

class Directory(object):
	def __init__(self, path, ideals, types):
		self.path = path
		self.ideals = ideals
		self.types = types

	def __getitem__(self, name):
		path = os.path.join(self.path, name)

		if not os.path.isdir(path):
			raise KeyError

		if os.path.isfile(os.path.join(path, ".db")):
			return Database.open(path, self.ideals, self.types)
		else:
			return Directory(path, self.ideals, self.types)

class Data(object):
	def __init__(self, root):
		self.root = root

	def __getitem__(self, item):
		try:
			with open(os.path.join(self.root, *item.split(".")) + ".json") as file:
				return json.load(file)
		except IOError:
			raise AttributeError

	def __setitem__(self, item, data):
		with open(os.path.join(self.root, *item.split(".")) + ".json") as file:
			json.dump(data, file)

class Ideals(Data):
	def __setitem__(self, item, data):
		raise AttributeError, "can't change ideals"

class Reals(Data):
	pass

ideals = local.LocalProxy()
reals  = local.LocalProxy()

class Database(object):
	@staticmethod
	def open(path, idealsRoot, types):
		try:
			with open(os.path.join(path, ".db")) as info:
				type = info.readline().strip()

			tree = types[type]

			local.set(reals, Reals(path))
			local.set(ideals, Ideals(os.path.join(idealsRoot, type)))

			return tree
		except BaseException as e:
			print("Corrupted database: {path}".format(path=path))
			raise e

def load(configdir = None):
	if configdir is None:
		configdir = sys.prefix + "/etc/koryto/blue"

	configfile = os.path.join(configdir, 'blue.cfg')
	config = ConfigParser()
	config.read_file(open(configfile), configfile)
	blueconfig = config[u"blue"]

	types = {}

	for t in blueconfig[u"types"].split(','):
		t = t.strip()

		types[t] = tree.load(os.path.join(configdir, t))

	return Directory(blueconfig[u"root"], blueconfig[u"ideals"], types)
