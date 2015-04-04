
class Node:
	def __init__(self, num):
		self.out = list()
		self.number = num
		self.eflag = 0
		self.nsets = list()
		
	def addout(self, ch, node):
		self.out.append((ch, node))
		
	def setend(self):
		self.eflag = 1
	
	def clearend(self):
		self.eflag = 0
		
	def isend(self):
		return self.eflag
	
	
		
class Graph:
	def __init__(self, s, e):
		self.start = s
		self.end = e
		self.chs = list()
		
	def match(self, str):
		return smatch(self.start, str)
		

def smatch(node, str):
	if (0 == len(str)):
		if (node.isend()):
			return 1
		else:	
			return 0
	else:
		ch = str[0]
		str = str[1:]
		for i in node.out:
			if (ch == i[0]):
				return smatch(i[1], str)
		return 0