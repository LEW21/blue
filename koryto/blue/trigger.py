class Trigger(object):
	"""
	Function trigger handler  - to use decorate triggered function with
	either a after(path) or before(path) methods, where path is a string in form 'type.name.method', 
	like 'building.fountain.upgrade'. That will be enhanced in future.
	"""
	def __init__(self):
		self.pre = {}
		self.post = {}
		self.after = self._settr(self.post)
		self.before = self._settr(self.pre)
		
	def _settr(self, target):
		def setTrigger(self, rawPath, *t_args):
			path = rawPath.split('.')
			
			# TODO correct, enhance
			if not len(path) == 3:
				raise Exception('Incorrect path: {var}'.format(var = rawPath))
			
			name = path[2]
			path = path[0]+'.'+path[1]

			try:
				triggers = target[path]
			except:
				triggers = target[path] = {}
			try:
				triggers = triggers[name]
			except:
				trigger = triggers[name] = {}
			def wrapper(f):
				trigger[f] = t_args
				def wrapped(*args):
					return f(*args)
				
				return wrapped
			
			return wrapper
		return setTrigger

	def setIn(self, cls):
		"""
		Decorator for class, adding trigger support in every method defined in that class
		"""
		def allowTrigger(fun):
			def checkTrigs(obj, *args):
				path = obj.__blue_path__
				name = fun.__name__
				err = None
				
				try:
					pre = self.pre[path][name]
				except:
					pre = {}
				try:
					post = self.post[path][name]
				except:
					post = {}

				for func in pre:
					try:
						func(*pre[func])
					except Exception as e:
						err = e
				if err:
					raise err
				
				tmp = fun(obj, *args)
				
				for func, arg in post:
					try:
						func(*pre[func])
					except Exception as e:
						err = e
				if err:
					raise err
				
				return tmp
			return checkTrigs
		
		for name in dir(cls):
			attr = getattr(cls, name)
			# Can it be done better?
			if callable(attr) and not name.startswith('__'):
				setattr(cls, name, allowTrigger(attr))
		
		return cls
