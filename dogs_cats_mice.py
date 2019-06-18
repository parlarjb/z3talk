from z3 import *

# We have $100, and need to buy 100 animals
# We have to buy a least one dog, one cat, and one mouse
# Dogs cost $15, cats cost $1, and mice are $0.25
# How many of each should we buy?

# The variables `dog`, `cat` and `mouse` represent
# how many of each we will buy
dog = Int('dog')
cat = Int('cat')
mouse = Int('mouse')

s = Solver()

# We have to buy one of each animal
s.add(dog >= 1)
s.add(cat >= 1)
s.add(mouse >= 1)

# We have to buy 100 animals
s.add(dog + cat + mouse == 100)

# We have 100 dollars (10000 cents)
# We have to spend all 100 dollars
# Dogs cost 15 dollars (1500 cents)
# Cats cost 1 dollar (100 cents)
# mice cost 25 cents
s.add(1500*dog + 100*cat + 25*mouse == 10000) 

