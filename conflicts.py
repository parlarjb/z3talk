from z3 import *

x = Int('x')
y = Int('y')

s = Solver()

# Rule 1 is true when x > 5 and y < 10
s.add(x > 5)
s.add(y < 10)

# Rule 2 is true when x > 7 and y > 6
s.add(x > 7)
s.add(y > 6)
