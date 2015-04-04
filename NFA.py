import Graph
import utils

class NFA:
	bseq = ""
	chs = ""	
	
	def eval(self, bseq):
		self.bseq = bseq
		self.chs = list()
		st = list()
		m = 0
		for c in self.bseq:
			if (utils.isalpha(c)):
				m = self.opalpha(st, c, m)
			elif (c == "@"):
				m = self.opcat(st, m)
			elif (c == "*"):
				m = self.opclosure(st, m)
			elif (c == "|"):
				m = self.opor(st, m)
		
		g = st.pop()
		it = list()
		#show(g.start, it)
		
		g.chs = self.chs
		return g

	def opalpha(self, st, ch, mark):
		s = Graph.Node(mark)
		e = Graph.Node(mark+1)
		s.addout(ch, e)
		e.setend()

		g = Graph.Graph(s, e)
		st.append(g)
		
		if (ch not in self.chs):
			self.chs.append(ch)
		return mark+2
		

	def opcat(self, st, mark):
		g2 = st.pop()
		g1 = st.pop()
		
		g1.end.addout('~', g2.start)
		
		g1.end.clearend()
		
		g = Graph.Graph(g1.start, g2.end)
		st.append(g)
		return mark
	
	def opclosure(self, st, mark):
		g = st.pop()
		s = Graph.Node(mark)
		e = Graph.Node(mark+1)
		
		s.addout('~', g.start)
		s.addout('~', e)
		g.end.addout('~', e)
		g.end.addout('~', g.start)
		
		g.end.clearend()
		e.setend()
		
		g1 = Graph.Graph(s, e)
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
		
		g = Graph.Graph(s, e)
		st.append(g)
		
		return mark+2