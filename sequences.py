from z3 import *
from presentationutils import force_new_solution

# We'll ask z3 to find us a sequence of integers with 
# more than 5 elements, which must contain the number 4,
# which must contain the numbers 2,
# where the number 2 must appear at index 3
# which must contain the number 1
# and the number 1 must appear after the number 4

# Define a new type, representing sequence of integers
IntSequenceType = SeqSort(IntSort())

# Create a variable using our new type
seq = Const('seq', IntSequenceType)

s = Solver()

# Require the sequence to be greater than 5 elements
s.add(Length(seq) > 5)

# The sequence must contain the number 4
s.add(Contains(seq, Unit(IntVal(4))))

# The number 2 must appear at index 3
s.add(IndexOf(seq, Unit(IntVal(2)), 0) == 3)

# The number 1 must after the number 4
s.add(
    IndexOf(seq, Unit(IntVal(1)), 0) 
        > IndexOf(seq, Unit(IntVal(4)), 0))