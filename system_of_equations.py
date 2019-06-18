from z3 import *

# Declare z3 variables x, y and z
x = Real('x')
y = Real('y')
z = Real('z')

s = Solver()

s.add(3*x + 2*y - z == 1)
s.add(2*x - 2*y + 4*z == -2)
s.add(-x + 0.5*y - z == 0)