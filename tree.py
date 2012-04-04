
class Node(object):
	def __init__(self, name="", parent=None):
		self.name = name
		self.parent = parent

class DeclarativeNode(Node):
	def __init__(self, meta=None, *args, **kwargs):
		Node.__init__(self, *args, **kwargs)
		if meta:
			self.meta = meta

	def __getitem__(self, name, *args, **kwargs):
		try:
			key = name
			node = self.meta[key]
		except KeyError:
			try:
				key = "*"
				node = self.meta[key]
			except KeyError:
				raise KeyError

		if not callable(node):
			if node.__getitem__ and node.__setitem__:
				data = node
				node = lambda *args, **kwargs: DeclarativeNode(meta=data, *args, **kwargs)
			else:
				"""Import the module"""
				pass

			self.meta[key] = node

		return node(name=name, parent=self, *args, **kwargs)
