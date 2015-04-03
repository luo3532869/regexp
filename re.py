import re
import sys

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
	
class Reg:
	line = ""
	tok = ""
	ns = 0
	bseq = ""
	def __init__(self, line):
		self.line = line
		self.advance()
		
	def advance(self):
		if (0 == len(self.line)):
			self.tok = ""
			return
		else:
			self.tok = self.line[0]
			self.line = self.line[1:]
		if (0 == islegal(self.tok)):
			print "syntax error: get a illegal character: " + self.tok
			sys.exit()
	
	def expr(self):
		self.terms()
		if (self.tok == "|"):
			self.advance()
			self.terms()
			self.mark("|")
			
	def terms(self):
		self.term()
		while (isalpha(self.tok) or self.tok == "("):
			self.term()
			self.mark("@")
			
	def term(self):
		self.factor()
		if (self.tok == "*"):
			self.mark("*")
			self.advance()
			
	def factor(self):
		if (self.tok == "("):
			self.advance()
			self.expr()
			if (self.tok != ")"):
				print "syntax error: lack of right bracket"
				sys.exit()
			else:
				self.advance()
		elif (isalpha(self.tok)):
			self.mark(self.tok)
			self.advance()
		else:
			print "syntax error: unexpected character: "+self.tok
			sys.exit()
	
	def mark(self, ch):
		self.bseq += ch
		self.ns += 1
		
	def showseq(self):
		for c in self.bseq:
			print c
		
class Eval:
	
	def __init__(self, bseq):
		self.bseq = bseq
		self.chs = list()
	
	def eval(self):
		st = list()
		m = 0
		for c in self.bseq:
			if (isalpha(c)):
				m = self.opalpha(st, c, m)
			elif (c == "@"):
				m = self.opcat(st, m)
			elif (c == "*"):
				m = self.opclosure(st, m)
			elif (c == "|"):
				m = self.opor(st, m)
		
		g = st.pop()
		it = list()
		show(g.start, it)
		
		g.chs = self.chs
		return g

	def opalpha(self, st, ch, mark):
		s = Node(mark)
		e = Node(mark+1)
		s.addout(ch, e)
		e.setend()

		g = Graph(s, e)
		st.append(g)
		
		if (ch not in self.chs):
			self.chs.append(ch)
		return mark+2
		

	def opcat(self, st, mark):
		g2 = st.pop()
		g1 = st.pop()
		
		g1.end.addout('~', g2.start)
		
		g1.end.clearend()
		
		g = Graph(g1.start, g2.end)
		st.append(g)
		return mark
	
	def opclosure(self, st, mark):
		g = st.pop()
		s = Node(mark)
		e = Node(mark+1)
		
		s.addout('~', g.start)
		s.addout('~', e)
		g.end.addout('~', e)
		g.end.addout('~', g.start)
		
		g.end.clearend()
		e.setend()
		
		g1 = Graph(s, e)
		st.append(g1)
		return mark+2
	
	def opor(self, st, mark):
		s = Node(mark)
		e = Node(mark+1)
		g1 = st.pop()
		g2 = st.pop()
		
		s.addout('~', g1.start)
		s.addout('~', g2.start)
		g1.end.addout('~', e)
		g2.end.addout('~', e)
		
		g1.end.clearend()
		g2.end.clearend()
		e.setend()
		
		g = Graph(s, e)
		st.append(g)
		
		return mark+2
		
class DFA:
	def __init__(self, g):
		self.graph = g
	
	def todfa(self):
		ng = self.graph
		fifo = list()
		nset = list()
		mark = 0
		eflag = 0
		s0 = Node(mark)
		mark += 1
		s0.eflag = self.nEset(ng.start, s0.nsets)
		
		fifo.insert(0, s0)
		
		while ([] != fifo):
			t = fifo.pop()
			nset.append(t)
			u = list()
			for ch in ng.chs:
				dn = Node(mark)
				dn.eflag = self.sEset(self.dnMove(t, ch), dn.nsets)
				if ([] == dn.nsets):
					continue
				e = self.getdnode(fifo, nset, dn.nsets)
				if (0 == e):
					fifo.insert(0, dn)
					mark += 1
				else:
					dn = e
				t.addout(ch, dn)
		
		it = list()
		show(s0, it)		
	
	def getdnode(self, fifo, nset, key):
		for i in fifo:
			if (i.nsets == key):
				return i
		for i in nset:
			if (i.nsets == key):
				return i
		return 0
	
	#node's empty set
	#nn is the not definitive machine's node
	def nEset(self, nn, r):
		eflag = 0
		if (nn not in r):
			r.append(nn)
		if (nn.isend()):
			eflag = 1
		for i in nn.out:
			if (i[0] == '~' and i[1] not in r):
				r.append(i[1])
				eflag = eflag or self.nEset(i[1], r)
				
		return eflag
		
	#set's empty set
	#ns is the not definitive machine's node set
	def sEset(self, ns, r):
		eflag = 0
		for i in ns:
			eflag = eflag or self.nEset(i, r)
		return eflag
		
	#node's empty set
	#nn is the not definitive machine's node
	def nnMove(self, nn, ch, r):
		for i in nn.out:
			if (i[0] == ch and i[1] not in r):
				r.append(i[1])
			
	#set's empty set
	#ds is the definitive machine's node
	def dnMove(self, dn, ch):
		r = list()
		for i in dn.nsets:
			self.nnMove(i, ch, r)
		return r
		
		
for line in open("test.data"):
	r = Reg(line)
	r.expr()
	r.showseq()
	ev = Eval(r.bseq)
	nfa = ev.eval()
	print "######################################"
	d = DFA(nfa)
	dfa = d.todfa()
	