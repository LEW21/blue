from configparser import ConfigParser
import os
import sys

def importClass(path):
	moduleName, className = path.split("#", 1)

	if not moduleName in sys.modules:
		__import__(moduleName)

	return getattr(sys.modules[moduleName], className)

def buildClass(name, config = {}):
	parents = [importClass("koryto.blue.api#Object")]

	for opt in config:
		if opt.startswith("mixin.") or opt == "base":
			parents.append(importClass(config[opt]))

	cls = type(str(name), tuple(parents), {})
	cls.__blue_meta_children__ = {}

	return cls

def load(configdir):
	conf = ConfigParser()
	conf.read([os.path.join(configdir, x) for x in os.listdir(configdir) if x.endswith(".cfg")])

	sections = sorted(conf.sections())

	try:
		root = conf["/"]
	except KeyError:
		root = {}

	root = buildClass("", root)

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
				parent.__blue_meta_children__[segment] = buildClass(segment)
				parent = parent.__blue_meta_children__[segment]

		segment = segments[-1]

		parent.__blue_meta_children__[segment] = buildClass(segment, conf[section])

	return root
