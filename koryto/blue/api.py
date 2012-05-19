from koryto.blue.database import ideals, reals
import koryto.blue.constraints
from inspect import getargspec

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
		self.__blue_path__ = path
		self.__blue_children__ = {}

	@lazy
	def real(self):
		return Real(self.__blue_path__)

	@lazy
	def ideal(self):
		return Ideal(self.__blue_path__)

	def __getitem__(self, name):
		try:
			return self.__blue_children__[name]
		except KeyError:
			try:
				Item = self.__blue_meta_children__[name]
			except (KeyError, AttributeError):
				try:
					Item = self.__blue_meta_children__["*"]
				except (KeyError, AttributeError):
					raise KeyError

			self.__blue_children__[name] = Item(self.__blue_path__ + "." + name if self.__blue_path__ else name)
			return self.__blue_children__[name]

	def __getattr__(self, name):
		try:
			return self[name]
		except KeyError:
			try:
				getattr(super(Object, self), name)
			except AttributeError:
				raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__blue_path__, name))

class SoMeta(type):
	def __getattr__(cls, key):
		return lambda *kwargs: cls.property(key, *kwargs)

def validate(self, value, constraints):
	for con in constraints:
		args = getargspec(con).args

		if not len(args):
			res = con()
		elif args[0] == "self":
			res = lambda: con(self, value)
		else:
			res = lambda: con(self)

		if not res:
			raise ValueError

class Real(object):
	__metaclass__ = SoMeta

	@staticmethod
	def property(name, type, default=None, doc=None, *constraints, **stdConstraints):
		for name in stdConstraints:
			constraints += getattr(koryto.blue.constraints, name)(stdConstraints[name])

		def getter(self):
			try:
				return type(self.real[name])
			except KeyError:
				return type(default)

		def setter(self, value):
			value = type(value)
			validate(self, value, constraints)
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
	def property(name, type, doc=None):
		def getter(self):
			return type(self.ideal[name])

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
