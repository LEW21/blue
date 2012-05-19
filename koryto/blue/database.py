import os
import local
import json
import koryto.blue.tree

class Data(object):
	def __init__(self, root):
		self.root = root

	def __getitem__(self, item):
		path = os.path.join(self.root, *item.split(".")) + ".json"
		try:
			with open(path) as file:
				return json.load(file)
		except IOError:
			raise AttributeError, "Missing file: " + path

	def __setitem__(self, item, data):
		path = os.path.join(self.root, *item.split(".")) + ".json"

		try:
			os.makedirs(os.path.dirname(path))
		except OSError:
			pass

		with open(path, "w") as file:
			json.dump(data, file)

class Ideals(Data):
	def __setitem__(self, item, data):
		raise AttributeError, "can't change ideals"

class Reals(Data):
	pass

def Tree(path):
	return koryto.blue.tree.load(path)

def Metabase(type, configroot, idealsroot):
	class Database(object):
		metatree = Tree(os.path.join(configroot, type))
		ideals = Ideals(os.path.join(idealsroot, type))

		def __init__(self, path):
			self.reals = Reals(path)
			self.tree = self.metatree(self, "")

	return Database

def metabases(types, configroot, idealsroot):
	metabases = {}
	for type in types:
		metabases[type] = Metabase(type, configroot, idealsroot)
	return metabases

def load(path, metabases):
	try:
		with open(os.path.join(path, ".db")) as info:
			type = info.readline().strip()

		Database = metabases[type]
	except BaseException as e:
		print("Corrupted database: {path}".format(path=path))
		raise e

	db = Database(path)
	return db.tree
