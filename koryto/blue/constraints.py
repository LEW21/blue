def min(min):
	return lambda x: x >= min

def eq(eq):
	return lambda x: x == eq

def max(max):
	return lambda x: x <= max

def minLen(min):
	return lambda x: len(x) >= min

def eqLen(eq):
	return lambda x: len(x) == eq

def maxLen(max):
	return lambda x: len(x) <= max

len = eqLen
