import os
import local

class Directory(object):
	def __init__(self, path):
		self.path = path

	def __getitem__(self, name):
		path = os.path.join(self.path, name)

		if not os.path.isdir(path):
			raise KeyError

		if os.path.isfile(os.path.join(path, ".db")):
			return Database.open(path)
		else:
			return Directory(path)

class Data(object):
	def __init__(self, root):
		self.root = root

	def __getitem__(self, item):
		with open(os.path.join(self.root, *item.split(".")) + ".json") as file:
			return json.load(file)

	def __setitem__(self, item, data):
		with open(os.path.join(self.root, *item.split(".")) + ".json") as file:
			json.dump(data, file)

class Ideals(Data):
	def __setitem__(self, item, data):
		raise AttributeError, "can't change ideals"

class Reals(Data):
	pass

ideals = None
reals  = local.LocalProxy()

def setupIdeals(path):
	global ideals
	ideals = Ideals(path)

class Database(object):
	types = {}

	@staticmethod
	def open(path):
		reals.set(Reals(path))

		try:
			with DB[""].open("db") as info:
				type = info.readline().strip()

			return Database.types[type]
		except BaseException as e:
			print("Corrupted database: {path}".format(path=path))
			raise e