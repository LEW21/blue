import sys

class Node(object):
	def __init__(self, config, _vars):
		module, type = config["type"].split('#', 1)
		try:
			module = sys.modules[module]
		except KeyError:
			__import__(module)
			module = sys.modules[module]
		self._type = reduce(getattr, type.split("."), module)
		self._vars = _vars
		self._path = config["path"]

	def __getattribute__(self, name):
		if name[0] == '_':
			return object.__getattribute__(self, name)
	
		path = self._path.format(**self._vars)

		obj = self._type(path)

		return getattr(obj, name)
