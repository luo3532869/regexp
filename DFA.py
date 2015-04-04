import Graph

class DFA:

	def eval(self, nfa):
		fifo = list()
		nset = list()
		mark = 0
		eflag = 0
		s0 = Graph.Node(mark)
		mark += 1
		s0.eflag = self.nEset(nfa.start, s0.nsets)
		
		fifo.insert(0, s0)
		
		while ([] != fifo):
			t = fifo.pop()
			nset.append(t)
			u = list()
			for ch in nfa.chs:
				dn = Graph.Node(mark)
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
		
		dfa = Graph.Graph(s0, "")
		dfa.chs = nfa
		#it = list()
		#show(s0, it)
		return dfa
	
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
				eflag = self.nEset(i[1], r) or eflag
				
		return eflag
		
	#set's empty set
	#ns is the not definitive machine's node set
	def sEset(self, ns, r):
		eflag = 0
		for i in ns:
			eflag = self.nEset(i, r) or eflag
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