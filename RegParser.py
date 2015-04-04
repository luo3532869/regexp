import sys
import Graph
import utils

class RegParser:
	line = ""
	tok = ""
	ns = 0
	bseq = ""
	
	def parse(self, line):
		self.line = line
		self.advance()
		self.expr()
		return self.bseq
		
	def advance(self):
		if (0 == len(self.line)):
			self.tok = ""
			return
		else:
			self.tok = self.line[0]
			self.line = self.line[1:]
		if (0 == utils.islegal(self.tok)):
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
		while (utils.isalpha(self.tok) or self.tok == "("):
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
		elif (utils.isalpha(self.tok)):
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