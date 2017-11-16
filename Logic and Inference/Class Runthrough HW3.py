from read import*
class fact (object):
    def __init__(self, statement, asserted = True, supportedby = []):
        self.statement = statement
        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False
        self.supportedby = supported
        self.facts_supported = []
        self.rules_supported = []

class rule (object):
    def __init__(self, rule, supportedby = []):
        self.LHS = rule[0]
        self.RHS = rule[1]
        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False
            
        self.supportedby = supported
        self.facts_supported = []
        self.rules_supported = []

class kb (object):
    self.facts = []
    self.rules = []

    def add_fact(self,fact):
        self.fact.append(fact)
        
    def add_rule(self, rule):
        self.rules.append(rule)

    def rem_fact(self, fact):
        self.facts.remove(fact)
    def rem_rule(self, rule):
        self.rules.remove(rule)

    def kb_assert(self, statement):
        f = fact(statement)
        self.add_fact(f)

def add_b(binding, variable, constant):
    binding.append([variable,constant])
def binding_val(binding, variable):
    for b in bindings:
        if b[0] = variable:
            return b[1]

def match(s1,s2):
    bindings = []
    if len(s1) != len(s2):
        return false
    
    if s1[0] ==s2[0]:
        for x in range(len(s1)):
            if s1[x] =='?':
                if s2[x] == binding_val(bindings, s1[x]):
                    return True
                else:
                    add_b(bindings,var,
            
    
        
