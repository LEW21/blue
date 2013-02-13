class Trigger(object):
	"""
	Function trigger handler  - to use decorate triggered function with
	either a after(path) or before(path) methods, where path is a string in form 'type.name.method', 
	like 'building.fountain.upgrade'. That will be enhanced in future.
	"""
	def __init__(self):
		self.pre = {}
		self.post = {}
		
		#Now create methods used for setting triggers
		self.after = self._settr(self.post)
		self.before = self._settr(self.pre)
	
	# Closure function to create trigger setting functions
	def _settr(self, target):
		# Decorating with @dec(arg) is equal to: func = dec(arg)(func), 
		# Get first set of arguments - trigger target and optional function execution parameters
		def setTrigger(self, rawPath, *t_args):
			path = rawPath.split('.')
			
			# TODO correct, enhance
			if not len(path) == 3:
				raise Exception('Incorrect path: {var}'.format(var = rawPath))
			
			name = path[2]
			path = path[0]+'.'+path[1]
			
			#Get dictionary for given trigger, if one not exists create it
			try:
				triggers = target[path]
			except KeyError:
				triggers = target[path] = {}
			
			try:
				trigger = triggers[name]
			except KeyError:
				trigger = triggers[name] = {}
			
			# Get second parameter, the function
			def wrapper(f):
				trigger[f] = t_args				# Add function with arguments to the list of triggers
				
				# Actual decorator, leaves funcion as it was
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
				
				# Get function specific dictionary
				try:
					pre = self.pre[path][name]
				except:
					pre = {}
				try:
					post = self.post[path][name]
				except:
					post = {}
				
				# Execute pre-triggers
				for func in pre:
					try:
						func(*pre[func])
					except Exception as e:
						err = e
				if err:							# If any exceptions was encountered, 
					raise err					# raise the last one. Not sure how this should be done better.
				
				tmp = fun(obj, *args)
				
				# Execute post-triggers
				for func in post:
					try:
						func(*post[func])
					except Exception as e:
						err = e
				if err:
					raise err
				
				return tmp
			return checkTrigs
		
		# Every method in decorated class gets decorated by allowTrigger
		for name in dir(cls):
			attr = getattr(cls, name)
			# Can it be done better?
			if callable(attr) and not name.startswith('__'):
				setattr(cls, name, allowTrigger(attr))
		
		return cls
