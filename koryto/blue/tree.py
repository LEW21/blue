from configparser import ConfigParser
import os
import sys

def importClass(path):
	moduleName, className = path.split("#", 1)

	if not moduleName in sys.modules:
		__import__(moduleName)

	return getattr(sys.modules[moduleName], className)

def buildClass(config):
	base = importClass(config["base"])
	parents = [base]

	for name in config:
		if name.startswith("mixin."):
			parents.append(importClass(config[name]))

	cls = type(base.__name__, tuple(parents), {})
	cls.__blue_meta_children__ = {}

	return cls

def load(configdir):
	conf = ConfigParser()
	conf.read([os.path.join(configdir, x) for x in os.listdir(configdir) if x.endswith(".cfg")])

	sections = sorted(conf.sections())

	default = {"base": "koryto.blue#Object"}

	try:
		root = conf["/"]
	except KeyError:
		root = default

	root = buildClass(root)

	for section in sections:
		segments = section.split('/')

		if segments[0]: # This is not a path.
			continue

		if len(segments) == 1: # This is root.
			continue

		parent = root

		for segment in segments[:-1]:
			if not segment:
				continue

			try:
				parent = parent.__blue_meta_children__[segment]
			except KeyError:
				parent.__blue_meta_children__[segment] = buildClass(default)
				parent = parent.__blue_meta_children__[segment]

		name = segments[-1]

		parent.__blue_meta_children__[name] = buildClass(conf[section])

	return root
