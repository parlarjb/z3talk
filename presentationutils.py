from z3 import *

# Add a constraint that at least one of
# the found values must be different from the
# last time 
def force_new_solution(s):
    m = s.model()
    s.add(Or([f() != m[f] for f in m.decls() if f.arity() == 0]))