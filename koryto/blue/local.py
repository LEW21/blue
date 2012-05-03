from gevent.local import local

def set(self, obj):
	local.__setattr__(self, "obj", obj)

class LocalProxy(local):
	def __getattribute__(self, name):
		return getattr(local.__getattribute__(self, "obj"), name)

	def __getitem__(self, name):
		return self.__getitem__(name)

	def __setitem__(self, name, value):
		return self.__setitem__(name, value)
