import os
import local
import json
import koryto.tree

ideals = local.LocalProxy()
reals  = local.LocalProxy()
tree   = local.LocalProxy()

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

def Tree(path):
	return koryto.tree.load(path)

class MetaBase(object):
	def __init__(self, type, configroot, idealsroot):
		self.tree = Tree(os.path.join(configroot, type))
		self.ideals = Ideals(os.path.join(idealsroot, type))

def metabases(types, configroot, idealsroot):
	metabases = {}
	for type in types:
		metabases[type] = MetaBase(type, configroot, idealsroot)
	return metabases

def load(path, metabases):
	try:
		with open(os.path.join(path, ".db")) as info:
			type = info.readline().strip()

		meta = metabases[type]
	except BaseException as e:
		print("Corrupted database: {path}".format(path=path))
		raise e

	local.set(tree, meta.tree)
	local.set(ideals, meta.ideals)
	local.set(reals, Reals(path))

	return local.get(tree)
