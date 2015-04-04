import utils
import RegParser
import NFA
import DFA

		
def regexp(pattern):
	rp = RegParser.RegParser()
	post = rp.parse(pattern)  #post order
	nfa = NFA.NFA()
	n = nfa.eval(post)
	dfa = DFA.DFA()
	d = dfa.eval(n)
	return d
	


	