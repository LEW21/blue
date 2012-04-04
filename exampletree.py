from tree import Node, DeclarativeNode
from jsonrmc import exposed

class Building(Node):
	pass

class BigItem(Node):
	pass

class SmallItem(Node):
	pass

class Ideals(Node):
	pass

class Account(DeclarativeNode):
	meta = {
		"buildings": {"*": Building},
		"items": {
			"big": {"*": BigItem},
			"small": {"*": SmallItem},
		},
		"ideals": Ideals,
	}

	@exposed
	def get(self):
		return "Hello world!"
