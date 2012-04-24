from gevent.local import local

class LocalProxy(local):
	def __getattribute__(self, name):
		try:
			obj = local.__getattribute__(self, "obj")
		except AttributeError:
			if name == "set":
				return lambda obj: local.__setattr__(self, "obj", obj)
			else:
				raise AttributeError

		return getattr(obj, name)

	def __getitem__(self, name):
		return self.__getitem__(name)

	def __setitem__(self, name, value):
		return self.__setitem__(name, value)
