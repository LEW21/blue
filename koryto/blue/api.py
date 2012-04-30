
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
	def __init__(self, parent, name):
		self.parent = parent
		self.name = name

	@property
	def path(self):
		if self.parent:
			return os.path.join(self.parent.path, self.name)
		else:
			return self.name

	@lazy
	def real(self):
		return Real(self.path)

	@lazy
	def ideal(self):
		return Ideal(self.path)

class Real(object):
	@staticmethod
	def property(name, doc=None):
		def getter(self):
			return getattr(self.real, name)
		def setter(self):
			return setattr(self.real, name)
		def deleter(self):
			return delattr(self.real, name)

		return property(fget=getter, fset=setter, fdel=deleter, doc=doc)

	def __init__(self, path):
		self.__dict__["_changed"] = False
		pass

	def __getattr__(self, name):
		pass

	def __setattr__(self, name, value):
		self.__dict__["_changed"] = True
		pass

	def __delattr__(self, name):
		self.__dict__["_changed"] = True
		pass

	def __del__(self):
		if self._changed:
			pass

class Ideal(object):
	@staticmethod
	def property(name, doc=None):
		def getter(self):
			return getattr(self.ideal, name)
		def setter(self):
			raise AttributeError
		def deleter(self):
			raise AttributeError

		return property(fget=getter, fset=setter, fdel=deleter, doc=doc)

	def __init__(self, path):
		pass

	def __getattr__(self, name):
		pass

	def __setattr__(self, name, value):
		raise AttributeError, "can't set attribute"

	def __delattr__(self, name):
		raise AttributeError, "can't delete attribute"
