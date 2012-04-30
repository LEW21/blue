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

DB = local.LocalProxy()

class Database(object):
	types = {}

	@staticmethod
	def open(path):
		DB.set(Data(path))

		try:
			with DB[""].open("db") as info:
				type = info.readline().strip()

			return Database.types[type]
		except BaseException as e:
			print("Corrupted database: {path}".format(path=path))
			raise e

class Data(object):
	def __init__(self, path):
		self.path = path

	def __getitem__(self, name):
		path = os.path.join(self.path, name)
		
		return Data(path)

	def __getattr__(self, name):
		return self[name]

	def file(self, type):
		return self.path + "." + type

	def open(self, type, mode = "r"):
		return open(self.file(type), mode)

	@property
	def data(self):
		with self.open("json") as file:
			return json.load(file) # parse_float = decimal.Decimal

	@data.setter
	def data(self, data):
		with self.open("json", "w") as file:
			json.dump(data, file)
