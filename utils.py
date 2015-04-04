import re
		
def isalpha(ch):
		if (re.match('[a-zA-Z]', ch)):
			return 1
		else:
			return 0
	
def islegal(ch):
	if (isalpha(ch) or ch == "(" or ch == ")" or ch == "*" or ch == "|"):
		return 1
	return 0
		

def show(node, it):
		if (node in it):
			return
		else:
			it.append(node)
			
		estr = ""
		if (node.eflag):
			estr = "<end>"
		print node.number, estr
		str = ""
		for i in node.out:
			print (i[0], i[1].number)
		print str
		for i in node.out:
			show (i[1], it)