from read import *
import copy
# Yibing Shi NetId:ysa6698
# Courtney Bankston NetId: cbf029
# All group members were present and contributing during all work on this project.

class fact (object):
    # Fact class that notes what the fact is supported by as well as the facts/rules it supports
    def __init__(self, statement, supported_by = []):
        self.statement = statement
        if not supported_by:
            self.asserted = True #asserted fact
        else:
            self.asserted = False #inferred fact
        self.supported_by = supported_by
        self.facts_supported = []
        self.rules_supported = []
    # Print fact
    def __str__(self):
        return str(self.statement)
    # Length of fact
    def __len__(self):
        return len(self.statement)
    # List of fact
    def __repr__(self):
        return str(self.statement)
    # Index of list of fact
    def __getitem__(self,index):
        return self.statement[index]
    # Index of list of fact
    def __setitem__(self,index,value):
        self.statement[index] = value

class rule (object):
    # Rule class that notes what the rule is supported by as well as the facts/rules it supports
    def __init__(self, rule, supported_by = []):
        self.LHS = rule[0]
        self.RHS = rule[1]
        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False

        self.supported_by = supported_by
        self.facts_supported = []
        self.rules_supported = []
    # Print rule
    def __str__(self):
        return str(self.LHS) + "->" + str(self.RHS)
    # Length of the rule
    def __len__(self):
        return len(self.LHS) + len(self.RHS)
    # List of rule object to print
    def __repr__(self):
        return str(self.LHS) + "->" + str(self.RHS)
    # Index of list of rules
    def __getitem__(self,index):
        if index == 0:
            return self.LHS
        if index == 1:
            return self.RHS
    # Index of list of rules
    def __setitem__(self,index,value):
        self.LHS[index] = value
    # Has the rule to compare
    def __hash__(self):
        return hash((self.LHS, self.RHS))
    # Check if two rule objects equals
    def __eq__(self, other):
        try:
            return (self.LHS, self.RHS) == (other.LHS, other.RHS)
        except AttributeError:
            return NotImplemented

class binding:
    # Binding class that correctly formats bindings for the knowledge base.
    # Bindings are represented as a dictionary in their raw inital format
    # Binding can also be represented as list in self.pretty when implemented in the knowledge base functions
    def __init__(self):
        self.bindings = {}
        self.pretty = []
    # Add bindings to object
    def add_binding(self, variable, value):
        self.bindings[variable] = value
        self.pretty.append([variable, value])
    # Return value of bindings
    def binding_value(self, variable):
        if variable in self.bindings.keys():
            return self.bindings[variable]
        return False
    # Get binding with Index
    def __getitem__(self,index):
        return self.pretty[index]
    def test_and_bind(self, variable, value):
        if variable in self.bindings.keys():
            if value == self.bindings[variable]:
                return True
            else:
                return False
        self.add_binding(variable, value)
        return True
    def __len__(self):
        return len(self.pretty)
    def __str__(self):
        return str(self.pretty)
    # Check if two binding objects are equal
    def __eq__(self, other):
        try:
            for bs in self.bindings.keys():
                if other.bindings[bs] != self.bindings[bs]:
                    return False
            return True
        except AttributeError:
            return NotImplemented
    def __repr__(self):
        return str(self.pretty)
    # Used in AskPlus, directly convert a list to binding object
    def convertList(self, lists):
        self.pretty = lists

def add_binding (bindingList, variable, constant):
    bindingList.append([variable,constant])

class kb:
    def __init__(self):
        self.facts = []
        self.rules = []
    # Print the KB
    def __str__(self):
        return "The KB contains " + str(len(self.facts)) + " of facts and " + str(len(self.rules)) + " of rules\nIf you need to see in details, please call kb.printKB() to see facts and rules.\n"

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def rem_fact(self, fact):
        self.facts.remove(fact)

    def rem_rule(self, rule):
        self.rules.remove(rule)

    def asserts (self, st):
        # Takes A statement
        # Adds it to the Knowledge Base
        # Runs loop to see if facts or rules can be inferred from new added fact/rule
        # If so, add that inferred fact/rule into the KB
        if type(st) == fact:
            for ft in self.facts:
                # When iterating the assert, if the facts already exists
                # add new supported_by to the supported_by list
                if ft.statement == st.statement:
                    if st.supported_by not in ft.supported_by:
                        ft.supported_by.extend(st.supported_by)
                    return
            if st.asserted == False:
                print "Infer a new fact : " + str(st) + ", Asserted : " + str(st.asserted)
            else:
                print "Assert a new fact : " + str(st) + ", Asserted : " + str(st.asserted)
            self.add_fact(st)
            for tr in self.rules: #if add fact, loop through rules to see if new facts/rules can be inferred
                x = self.infer(tr, st)
                if type(x) == fact:
                    self.asserts(x)
                    # Avoid duplicates
                    if x not in st.facts_supported:
                        st.facts_supported.append(x)
                    if x not in tr.facts_supported:
                        tr.facts_supported.append(x)
                elif type(x) == rule:
                    self.asserts(x)
                    # Avoid duplicates
                    if x not in st.rules_supported:
                        st.rules_supported.append(x)
                    if x not in tr.rules_supported:
                        tr.rules_supported.append(x)
                else:
                    continue
        elif type(st) == rule:
            for rl in self.rules:
                # When iterating the assert, if the rules already exists
                # add new supported_by to the supported_by list
                if rl.LHS == st.LHS and rl.RHS == st.RHS:
                    rl.supported_by.extend(st.supported_by)
                    return
            if st.asserted == False:
                print "Infer a new rule : " + str(st) + ", Asserted : " + str(st.asserted)
            else:
                print "Assert a new rule : " + str(st) + ", Asserted : " + str(st.asserted)
            self.add_rule(st)
            for tf in self.facts: #if add rule, loop through the facts to see if new facts/rules can be inferred
                x = self.infer(st, tf)
                if type(x) == fact:
                    self.asserts(x)
                    # Avoid duplicates
                    if x not in st.facts_supported:
                        st.facts_supported.append(x)
                    if x not in tf.facts_supported:
                        tf.facts_supported.append(x)
                elif type(x) == rule:
                    self.asserts(x)
                    # Avoid duplicates
                    if x not in st.rules_supported:
                        st.rules_supported.append(x)
                    if x not in tf.rules_supported:
                        tf.rules_supported.append(x)
                else:
                    continue

    def retract(self, statement):
        # Given a KB and a fact
        # Will remove that fact from the Knowledge Base
        # Uses breadth first search algorithm to search for the statements that are supported by the fact
        # Then retract will remove those supported statements as well
        checked_fact = self.ask(statement)
        if checked_fact:
            # Use queue to keep tract the tree structure
            queue = [checked_fact]
            while queue:
                node = queue.pop(0)
                if type(node) == fact:
                    self.rem_fact(node)
                    print str (node) + " is removed from facts in Knowledge Base"
                else:
                    self.rem_rule(node)
                    print str (node) + " is removed from rules in Knowledge Base"
                # For all facts it supported, add to the queue
                for sb in node.facts_supported:
                    if type(sb) == list:
                        for s in sb:
                            queue.append(s)
                    else:
                        queue.append(sb)
                # For all rules it supported, add to the queue
                for sr in node.rules_supported:
                    if type(sr) == list:
                        for r in sr:
                            queue.append(r)
                    else:
                        queue.append(sr)
        # If not found
        else:
            print str(statement) + "is not in Knowledge Base"


    def match (self, statement1, statement2):
        # Given Two statements
        # Returns the list of bindings that hold if the facts match
        # Will return False if the two statements are not a match
        bindings = binding()

        if not statement1 or not statement2: #then not a match
            return False
        if len(statement1) != len(statement2): #then not a match
            return False
        else:
            for i in range (0, len(statement1)): #loop through to see if facts are match
                # Both statements does not contain variables
                if not varq(statement1[i]) and not varq(statement2[i]):
                    if statement1[i]!= statement2[i]:
                        return False
                # One statement contains variables
                elif varq(statement1[i]) and not varq(statement2[i]):
                    if not bindings.test_and_bind(statement1[i], statement2[i]):
                        return False
                # One statement contains variables
                elif not varq(statement1[i]) and varq(statement2[i]):
                    if not bindings.test_and_bind(statement2[i], statement1[i]):
                        return False
                else:
                    continue
            if len(bindings) == 0:
                return True
            return bindings

    def instantiate(self, fact, BindingsList):
        # This is a kb self used instantiate function, for test files please go down
        # Given a fact and a list of bindings
        # When the bindings in the BindingsList can map to a specific fact, replace the variables in that fact
        for i in range (1, len(fact) ):
             for j in range (len(BindingsList)):
                 if fact[i] == BindingsList[j][0]:
                       fact[i] = BindingsList[j][1]
        return fact

    def infer (self, rule1, facts):
        # Given a fact and a rule, infer will return the fact that can be inferred from them
        # This uses match and instatiate to see if the bindings can match to the rule and fact,
        # And then will return a new fact with the inferred variables bound to the values by using instantiate
        newrule = copy.deepcopy(rule1)
        res = self.match(newrule.LHS[0], facts) #checks if the LHS of the rule and the fact match
        if res:
            if res == True:
                return fact(newrule.RHS, [[facts, rule1]]) #if so, return a new inferred fact
            else:
                newrule.LHS.remove(newrule.LHS[0])
                for lhs in newrule.LHS:
                    self.instantiate(lhs, res.pretty)
                self.instantiate(newrule.RHS, res.pretty)
        else:
            return False
        if newrule.LHS:
            return rule(newrule, [[facts, rule1]]) #inferred rule
        else:
            return fact(newrule.RHS, [[facts, rule1]]) #inferred fact

    def ask (self, patterns):
        # Given a Knowledge Base and a fact
        # Returns the list of a BindingsList if the fact is in the Knowledge Base
        res = []
        for kb in self.facts:
            match_returned = []
            match_returned = self.match(kb, patterns) #use match once decided that the fact is in the Knowledge Base
            if match_returned == True:
                return kb
            if match_returned is not False:
                res.append(match_returned)
        if len(res) != 0:
            return res
        return False


    def askplus (self, statementsList):
        # Given a list of statements and a Knowledge Base
        # Will see if the statements are in the KB, and also that they are consistent with regard to the bindings
        # This will return a list of bindings if the statements are consistent based on the matches found
        statementBindingList = []
        for states in statementsList:
            ask_result = self.ask(states)
            if ask_result == False:
                statementBindingList.append(False);
            else:
                if type(ask_result) == fact:
                    # Append True if fact exists in KB
                    statementBindingList.append(True)
                else:
                    statementBindingList.append(ask_result)
        res = []
        for i in range(0, len(statementBindingList)): # Check if statements are consistent with regard to bindings
            if statementBindingList[i] == True:
                continue
            elif statementBindingList[i] == False:
                return res
            else:
                # Call helper function for find bindings that are consistent
                res = self.askplus_helper(res, statementBindingList[i])
        return res

    def askplus_helper(self, bindingList1, bindingList2):
        # Helper function when dealing with more than one binding list
        if len(bindingList1) == 0:
            return bindingList2
        res = []
        for b2 in bindingList2:
            flag = False
            for b1 in bindingList1:
                # diff_add will return the consistent of two bindingLists
                diff = diff_add(b1, b2)
                if diff != []:
                    res.append(diff)
        if len(res) == 0:
            return False
        return res

    def why (self, statement1):
        # Uses Breadth First Search to traverse the tree populated of each node's supported_by facts
        # This will then print a tree of all of the facts that support the statement
        # It then returns the top-level facts that matched when node.asserted = True, because this means the node wasn't inferred and is top level
        toplevel = []
        checked_fact = self.ask(statement1)
        if checked_fact:
            print
            print str (checked_fact) + " is in Knowledge Base"
            print "=== printing the tree ==="
            # Queue for tracking
            queue = [checked_fact]
            while queue:
                node = queue.pop(0)
                # If it's asserted, add to toplevel list to return
                if node.asserted == True:
                    print str (node) + " is a leaf node"
                    toplevel.append(node)
                else:
                    print str (node) + " is a tree node"
                # Add all children node to queue
                for sb in node.supported_by:
                    print "\tsupported_by : " + str(sb)
                    if type(sb) == list:
                        for s in sb:
                            queue.append(s)
                    else:
                        queue.append(sb)

        else:
            print str(node) + "is not in Knowledge Base"
        print "---Returning the Top Level List---"
        return toplevel

    # Helper Function to Print knowledgeBase
    def printKB(self):
        print "===facts in KB:"
        for f in self.facts:
            print str(f) + ", asserted : " + str(f.asserted)
            print "\tsupported_by : " + str(f.supported_by)
            print "\tfacts_supported : " + str(f.facts_supported)
            print "\trules_supported : " + str(f.rules_supported)
        print "===rules in KB:"
        for r in self.rules:
            print str(r) + ", asserted : " + str(r.asserted)
            print "\tsupported_by : " + str(r.supported_by)
            print "\tfacts_supported : " + str(r.facts_supported)
            print "\trules_supported : " + str(r.rules_supported)

# Helper function for checking if it's a variable
def varq(variable):
    if "?" in variable:
        return True
    else:
        return False

# Helper function for checking if it's a fact
def factq(element):
    return type(element[0]) is str

# Helper function for returning the consistent of two bindingLists
def diff_add(this, other):
    res = binding()
    for op in other.pretty:
        if op[0] not in [item[0] for item in this.pretty]:
            temp = []
            for sp in this.pretty:
                temp.append(sp)
            temp.append(op)
            res.convertList(temp)
        else:
            for sp in this.pretty:
                if op[0] == sp[0] and op[1] != sp[1]:
                    return []
                elif op[0] == sp[0] and op[1] == sp[1]:
                    if len(this.pretty) >= len(other.pretty):
                        res.convertList(this.pretty)
                    else:
                        res.convertList(other.pretty)
                else:
                    continue
    return res

# WRAPPER FUNCTIONS FOR TEST FILE
# KB_assert Asserts a statement or a rule to a knowledge base. It invokes different code if it is one or the other.
# New facts and rules can trigger inference

def KB_assert(kb, assertion):
    if factq(assertion):
        kb.asserts(fact(assertion))
    else:
        kb.asserts(rule(assertion))

# KB_ask queries the knowledge base to check if a statement is true.

def KB_ask(kb, query):
    if factq(query):
        return kb.ask(query)
    else:
        return kb.ask(query)

# KB_why shows us the supports for a statement

def KB_why(kb, query):
    print str(kb.why(query))

# instantiate for test file
def instantiate(ask, query):
    new = copy.deepcopy(ask)
    for i in range (1, len(new)):
         for j in range (len(query)):
             if new[i] == query[j][0]:
                   new[i] = query[j][1]
    return new

# KB_retract removes a statement from the knowledge base and then all other facts and rules that
# it supports

def KB_retract(kb, statement):
    if factq(statement):
        kb.retract(statement)

# KB_ask_plus queries the knowledge base to check if a list of statements are true.

def KB_ask_plus(kb, query):
    return kb.askplus(query)

#=====For AskPlus, we also tested with:
# [["cute", "?y", "red"],["love", "?x", "green"]](All False)
# [["color", "?y", "red"],["color", "bigbox", "red"]](One bindingList with True)
# The result:
# Asking about: [['cute', '?y', 'red'], ['love', '?x', 'green']]
# Found 0 sets of bindings
# Asking about: [['color', '?y', 'red'], ['color', 'bigbox', 'red']]
# Found 1 sets of bindings
#
#	Binding: [['?y', 'bigbox']]
#	Facts: ['color', 'bigbox', 'red'] ['color', 'bigbox', 'red']
#

#=====OUR TESTERS======
#x = kb("statements.txt")

# After this the assert and infer will be called.
# You can use this line to see the knowledgeBase:
# x.printKB()
# WE'VE ALSO INCLUDED THE OUTPUT OF OUR TEST FUNCTIONS FOR GRADING PURPOSES

#=== Test for building knowledgeBase
# x.printKB()

#=== Test for match
# fact1 = ['inst', 'pyramid4', 'pyramid']
# fact2 = ['inst', '?x', 'pyramid']
# print x.match(fact1, fact2)
# #Output: [('?X', 'pyramid4')]
# fact3 = ['inst', 'pyramid4', 'pyramid']
# fact4 = ['inst', '?x', 'cube']
# print x.match(fact3, fact4)
# #Output: False
# fact5 = ['inst', 'pyramid4', '?y']
# fact6 = ['inst', '?x', 'cube']
# print x.match(fact5, fact6)
# #Output: [('?X', 'pyramid4'), ('?Y', 'cube')]
# fact7 = ['inst', '?x', '?y']
# fact8 = ['inst', '?y', 'cube']
# print x.match(fact7, fact8)
# #Output: [('?Y', 'cube')]
# fact9 = ['inst', 'cube2', 'cube']
# fact10 = ['inst', 'cube2', 'cube']
# print x.match(fact9, fact10)
# # Output True

#=== Test for ask
# fact1 = ['inst', '?x', 'pyramid']
# for r in x.ask(fact1):
#    print str(r)
# #--Output:
# #[('?x', 'pyramid1')]
# #[('?x', 'pyramid2')]
# #[('?x', 'pyramid3')]
# #[('?x', 'pyramid4')]--

# fact2 = ['size', '?x', 'big']
# for r in x.ask(fact2):
#    print str(r)
# #---Output:
# #[('?x', 'bigbox')]
# #[('?x', 'pyramid3')]
# #[('?x', 'pyramid4')]--

# fact3 = ['inst', '?x', '?y']
# for r in x.ask(fact3):
#    print str(r)
# #---Output
# [('?x', 'bigbox'), ('?y', 'box')]
# [('?x', 'littlebox'), ('?y', 'box')]
# [('?x', 'pyramid1'), ('?y', 'pyramid')]
# [('?x', 'pyramid2'), ('?y', 'pyramid')]
# [('?x', 'pyramid3'), ('?y', 'pyramid')]
# [('?x', 'pyramid4'), ('?y', 'pyramid')]
# [('?x', 'cube1'), ('?y', 'cube')]
# [('?x', 'cube2'), ('?y', 'cube')]
# [('?x', 'cube3'), ('?y', 'cube')]
# [('?x', 'cube4'), ('?y', 'cube')]
# [('?x', 'sphere1'), ('?y', 'sphere')]
# [('?x', 'bigbox'), ('?y', 'container')]
# [('?x', 'littlebox'), ('?y', 'container')]
# [('?x', 'pyramid1'), ('?y', 'block')]
# [('?x', 'pyramid2'), ('?y', 'block')]
# [('?x', 'pyramid3'), ('?y', 'block')]
# [('?x', 'pyramid4'), ('?y', 'block')]
# [('?x', 'cube1'), ('?y', 'block')]
# [('?x', 'cube2'), ('?y', 'block')]
# [('?x', 'cube3'), ('?y', 'block')]
# [('?x', 'cube4'), ('?y', 'block')]
# [('?x', 'sphere1'), ('?y', 'block')]---

# fact4 = ['isa', 'cube', 'block']
# print x.ask(fact4)
# Output: ['isa', 'cube', 'block']

# fact5 = ['beautiful', 'pyramid3', 'pyramid']
# print x.ask(fact5)
# #Output: False

#=== Test for askplus
#fact1 = ['inst', '?x', 'pyramid'] # List in Ask
#fact2 = ['size', '?x', 'big'] # List in Ask
#fact3 = ['inst', '?x', '?y'] # List in Ask
#fact4 = ['inst', 'pyramid2', 'pyramid'] # True
#fact5 = ['beautiful', 'pyramid3', 'pyramid'] # False
#statementList = [fact1, fact2, fact3]
#if x.askplus(statementList) == False:
#    print False
#else:
#    for y in x.askplus(statementList):
#        print str(y)
#Test for Ask from TESTFILE
#for match in x.ask(fact(['inst', '?x', 'box'])):
#    print match
#OUTPUT
#[['?x', 'bigbox']]
#[['?x', 'littlebox']]
#
#----Output:
#[['?x', 'pyramid3'], ['?y', 'pyramid']]
#[['?x', 'pyramid3'], ['?y', 'block']]
#[['?x', 'pyramid4'], ['?y', 'pyramid']]
#[['?x', 'pyramid4'], ['?y', 'block']]
# ---

#=== Test for Instantiate
# print x.instantiate (['inst', '?x', '?y'], [['?y','biggerbox'],['?x','box']] )
# Output: ['inst', 'box', 'biggerbox']
# print x.instantiate (['size', '?x', '?y'], [['?x','cube1'],['?y','big']] )
# Output: ['size', 'cube1', 'big']
# print x.instantiate (['covered', '?x', '?y'], [['?x','cube1'], ['?y','cube'], ['?z','cube2']])
# Output: ['covered', 'cube1', 'cube']


#=== Test for Infer
# print str(x.infer(rule([[['inst', '?x', '?y'], ['isa', '?y', '?z']], ['inst', '?x', '?z']]), ['inst', 'cube1', 'cube']))
# Output: [['isa', 'cube', '?z']]->['inst', 'cube1', '?z']
# print str(x.infer(rule([[['inst', '?x', 'cube']], ['flat', '?x']]), ['inst', 'cube1', 'cube']))
# Output: ['flat', 'cube1']
# print str(x.infer(rule([[['on', '?x', '?y'], ['bigger', '?x', '?y']], ['covered', '?y']]), ['inst', 'cube1', 'cube']))
# Output: False
# print str(x.infer(rule([[['married', '?x', '?y'], ['love', '?x', '?y']], ['happy', '?x', '?y']]), ['married', 'Bob', 'Alice']))
# Output: [['love', 'Bob', 'Alice']]->['happy', 'Bob', 'Alice']
# print str(x.infer(rule([[['love', 'Bob', 'Alice']], ['happy', 'Bob', 'Alice']]), ['love', 'Bob', 'Alice']))
# Output: ['happy', 'Bob', 'Alice']

#=== Test for Why
# f = ['flat', 'cube1']
# print "The top level list:" + str(x.why(f))
#----Output:
# ['flat', 'cube1'] is in Knowledge Base
# === printing the tree ===
# ['flat', 'cube1'] is a tree node
# 	supported_by : [['inst', 'cube1', 'cube'], [['inst', '?x', 'cube']]->['flat', '?x']]
# ---
# ['inst', 'cube1', 'cube'] is a leaf node
# ---
# [['inst', '?x', 'cube']]->['flat', '?x'] is a leaf node
# ---
# The top level:[['inst', 'cube1', 'cube'], [['inst', '?x', 'cube']]->['flat', '?x']]

# f = ['inst', 'cube1', 'cube']
# print "The top level list:" + str(x.why(f))
#----Output:
# ['inst', 'cube1', 'cube'] is in Knowledge Base
# === printing the tree ===
# ['inst', 'cube1', 'cube'] is a leaf node
# ---
# The top level list:[['inst', 'cube1', 'cube']]

#=== Test for Retract
# f = fact(['inst', 'pyramid1', 'pyramid'])
# x.retract(f)
#---Output:
# ['inst', 'pyramid1', 'pyramid'] is removed from facts in Knowledge Base
# [['isa', 'pyramid', '?z']]->['inst', 'pyramid1', '?z'] is removed from rules in Knowledge Base
# ['inst', 'pyramid1', 'block'] is removed from facts in Knowledge Base
# [['isa', 'block', '?z']]->['inst', 'pyramid1', '?z'] is removed from rules in Knowledge Base
# x.printKB()

#=== Test for askplus_helper
# fact1 = ['inst', '?x', 'pyramid']
# b1 = x.ask(fact1)
# fact3 = ['inst', '?x', '?y']
# b3 = x.ask(fact3)
# for xah in x.askplus_helper(b1, b3):
#     print str(xah)
#--- Output:
# [('?x', 'pyramid1'), ('?y', 'pyramid')]
# [('?x', 'pyramid1'), ('?y', 'block')]
# [('?x', 'pyramid2'), ('?y', 'pyramid')]
# [('?x', 'pyramid2'), ('?y', 'block')]
# [('?x', 'pyramid3'), ('?y', 'pyramid')]
# [('?x', 'pyramid3'), ('?y', 'block')]
# [('?x', 'pyramid4'), ('?y', 'pyramid')]
# [('?x', 'pyramid4'), ('?y', 'block')]
