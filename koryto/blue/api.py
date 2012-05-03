from koryto.blue.repository import ideals, reals

class property(property):
	def __init__(self, fget=None, fset=None, fdel=None, fvalid=None, doc=None):
		super(property, self).__init__(fget, fset, fdel, doc)
		self.fvalid = fvalid

	def validator(self, func):
		self.fvalid = func
		return self

	def __set__(self, obj, value):
		if self.fvalid is not None:
			self.fvalid(obj, value)
		return super(property, self).__set__(obj, value)

class lazy(object):
	def __init__(self, load):
		self.load = load

	def __get__(self, obj, type=None):
		value = self.load(obj)
		setattr(obj, self.load.__name__, value)
		return value

class Object(object):
	def __init__(self, path):
		self.path = path

	@lazy
	def real(self):
		return Real(self.path)

	@lazy
	def ideal(self):
		return Ideal(self.path)

class SoMeta(type):
	def __getattr__(cls, key):
		return lambda *kwargs: cls.property(key, *kwargs)

class Real(object):
	__metaclass__ = SoMeta

	@staticmethod
	def property(name, doc=None):
		def getter(self):
			return self.real[name]

		def setter(self, value):
			self.real[name] = value

		def deleter(self):
			del self.real[name]

		return property(fget=getter, fset=setter, fdel=deleter, doc=doc)

	def __init__(self, path):
		self._changed = False
		self.path = path
		try:
			self.data = reals[path]
		except AttributeError:
			self.data = {}

	def __getitem__(self, name):
		return self.data[name]

	def __setitem__(self, name, value):
		self._changed = True
		self.data[name] = value

	def __delitem__(self, name):
		self._changed = True
		del self.data[name]

	def __del__(self):
		if self._changed:
			reals[self.path] = self.data

class Ideal(object):
	__metaclass__ = SoMeta

	@staticmethod
	def property(name, doc=None):
		def getter(self):
			return self.ideal[name]

		def setter(self):
			raise AttributeError

		def deleter(self):
			raise AttributeError

		return property(fget=getter, fset=setter, fdel=deleter, doc=doc)

	def __init__(self, path):
		self.path = path
		self.data = ideals[path]

	def __getitem__(self, name):
		return self.data[name]

	def __setitem__(self, name, value):
		raise AttributeError, "can't set attribute"

	def __delitem__(self, name):
		raise AttributeError, "can't delete attribute"
