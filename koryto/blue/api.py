import koryto.blue.constraints
from inspect import getargspec
import weakref

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
	__slots__ = ["load"]

	def __init__(self, load):
		self.load = load
		try:
			self.__doc__ = load.__doc__
		except:
			pass

	def __get__(self, obj, type=None):
		if obj is None:
			return self
		value = self.load(obj)
		setattr(obj, self.load.__name__, value)
		return value

class ConstDict(object):
	__slots__ = ["data"]

	def __init__(self, data):
		self.data = data

	def __getitem__(self, name):
		return self.data[name]

class Object(object):
	def __init__(self, root, ideals, reals, path):
		if root == None:
			class A(object):
				pass
			root = A()
		self.__blue_root_weakref__ = weakref.ref(root)
		self.__blue_ideals__ = ideals
		self.__blue_reals__  = reals
		self.__blue_path__ = path
		self.__blue_children__ = {}

	@property
	def root(self):
		return self.__blue_root_weakref__()

	@lazy
	def real(self):
		try:
			return self.__blue_reals__[self.__blue_path__]
		except AttributeError:
			return None

	@lazy
	def ideal(self):
		return ConstDict(self.__blue_ideals__[self.__blue_path__])

	@property
	def now(self):
		"""TODO"""

	def queue(self, method, time):
		"""TODO"""

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

			self.__blue_children__[name] = Item(
				self.root,
				self.__blue_ideals__,
				self.__blue_reals__,
				self.__blue_path__ + "." + name if self.__blue_path__ else name)

			return self.__blue_children__[name]

	def __getattr__(self, name):
		try:
			return getattr(super(Object, self), name)
		except AttributeError:
			try:
				return self[name]
			except KeyError:
				raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__blue_path__, name))

	def __del__(self):
		if self.real:
			self.__blue_reals__[self.__blue_path__] = self.real
		else:
			del self.__blue_reals__[self.__blue_path__]

class objectify(object):
	__slots__ = ["_handler"]

	def __init__(self, handler):
		self._handler = handler

	def __getattr__(self, key):
		return lambda *args, **kwargs: self._handler(key, *args, **kwargs)

@objectify
def Ideal(name, T, doc=None):
	def getter(self):
		try:
			return T(self.ideal[name])
		except KeyError:
			raise AttributeError

	return property(fget=getter, doc=doc)

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

@objectify
def Real(name, T, default=None, doc=None, *constraints, **stdConstraints):
	for name in stdConstraints:
		constraints += getattr(koryto.blue.constraints, name)(stdConstraints[name])

	def getter(self):
		try:
			return T(self.real[name])
		except TypeError, KeyError:
			return T(default)

	def setter(self, value):
		if not self.real:
			raise AttributeError("Real does not exist.")

		value = T(value)
		validate(self, value, constraints)
		self.real[name] = value

	def deleter(self):
		if not self.real:
			raise AttributeError("Real does not exist.")

		del self.real[name]

	return property(fget=getter, fset=setter, fdel=deleter, doc=doc)
