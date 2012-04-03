import os

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

class Database(object):
	def __init__(self, path):
		self.path = path

	types = {}

	@staticmethod
	def open(path):
		with open(os.path.join(path, ".db")) as info:
			type = info.readline().strip()

		try:
			Db = Database.types[type]
		except KeyError as e:
			print("Invalid database type: {type} - of database {path}".format(type=type, path=path))
			raise e

		return Db(path)
