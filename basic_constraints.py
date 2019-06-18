from z3 import *

# Declare z3 variables x, y and z
x = Int('x')
y = Int('y')
z = Int('z')

s = Solver()

s.add(x > 0)

s.add(y < 0)

s.add(x + y + z == 42)

s.add(y + z == 26)

s.add(z < 0)
