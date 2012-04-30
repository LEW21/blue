
class Node(object):
	def __init__(self, config, _vars):
		module, type = config["type"].split('#', 1)
		try:
			module = sys.modules[module]
		except KeyError:
			module = __import__(module)
		self._type = reduce(getattr, type.split("."), module)
		self._vars = _vars

	def __getattribute__(self, name):
		obj = self._type(**self._vars)
		return getattr(obj, name)
