from z3 import *

a_0 = Int('a_0')
b_0 = Int('b_0')
c_0 = Int('c_0')
d_0 = Int('d_0')

# These two dictionaries are indexed by "state", representing
# a point in time. At state=0, no rules have run yet. At state=1,
# the first rule has run. At state=2, the second rule has run, etc. 
old_behaviour_vars = {
    0: {
        'a': a_0,
        'b': b_0,
        'c': c_0,
        'd': d_0
    }
}

# For both the old behaviour (with just two rules),
# and the new behaviour, the variables will be the same at state=0
new_behaviour_vars = {
    0: {
        'a': a_0,
        'b': b_0,
        'c': c_0,
        'd': d_0
    }
}

# Create a,b,c and d variables for each state (1, 2, 3),
# and for each of the behavious
for t in [1, 2, 3]:
    old_behaviour_vars[t] = {}
    new_behaviour_vars[t] = {}
    for var in ['a', 'b', 'c', 'd']:
        old_behaviour_vars[t][var] = Int(f"{var}_{t}_old")
        new_behaviour_vars[t][var] = Int(f"{var}_{t}_new")

s = Solver()

# At state=0, each of the four variables will be between 
# 0 and 20. This is representing 'all the possible values'
# that these variables might have on a new or updated ticket
s.add(a_0 >= 0, a_0 <= 20)
s.add(b_0 >= 0, b_0 <= 20)
s.add(c_0 >= 0, c_0 <= 20)
s.add(d_0 >= 0, d_0 <= 20)

def c_updater_conditions(state):
    # The conditions for the "C Updater" rule,
    # namely that B > 10 at the time the rule is run
    return state['b'] > 10

def c_updater_transition(prev_state, next_state):
    # C Updater sets C to 20 when its conditions are true
    # So if this rule fires, it means all the other variables
    # are unchanged, but C goes to 20 in the next state
    constraints = []
    for var in prev_state.keys():
        if var != 'c':
            constraints.append(next_state[var] == prev_state[var])
        else:
            constraints.append(next_state[var] == 20)
    
    return And(*constraints)

def d_updater_conditions(state):
    # The conditions for the "D Updater" rule,
    # namely that C > 10 at the time the rule is run
    return state['c'] > 10

def d_updater_transition(prev_state, next_state):
    constraints = []
    for var in prev_state.keys():
        if var != 'd':
            constraints.append(next_state[var] == prev_state[var])
        else:
            constraints.append(next_state[var] == 0)
    
    return And(*constraints)

def c2_updater_conditions(state):
    # The conditions for the "C2 Updater" rule,
    # namely that A > 10 at the time the rule is run
    return state['a'] > 10

def c2_updater_transition(prev_state, next_state):
    constraints = []
    for var in prev_state.keys():
        if var != 'c':
            constraints.append(next_state[var] == prev_state[var])
        else:
            constraints.append(next_state[var] == 0)
    
    return And(*constraints)


def unchanged(prev_state, next_state):
    # Declare that all variables are unchanged
    # between prev_state and next_state
    constraints = []
    for var in prev_state.keys():
        constraints.append(next_state[var] == prev_state[var])
    return And(*constraints)

constraints = []

# Set up all the constraints for the original behaviour
constraints.append(
    If(
        c_updater_conditions(old_behaviour_vars[0]), 
        c_updater_transition(old_behaviour_vars[0], old_behaviour_vars[1]),
        unchanged(old_behaviour_vars[0], old_behaviour_vars[1])
    )
)

# The old behaviour has one less "step" than the new behaviour,
# so we'll simulate having the same number of steps by inserting
# an unchanged() into the old behaviour at the point in time
# in which the new behaviour would be running its rule
constraints.append(
    unchanged(old_behaviour_vars[1], old_behaviour_vars[2])
)

constraints.append(
    If(
        d_updater_conditions(old_behaviour_vars[2]), 
        d_updater_transition(old_behaviour_vars[2], old_behaviour_vars[3]),
        unchanged(old_behaviour_vars[2], old_behaviour_vars[3])
    )
)

# Set up all the constraints for the new behaviour
constraints.append(
    If(
        c_updater_conditions(new_behaviour_vars[0]), 
        c_updater_transition(new_behaviour_vars[0], new_behaviour_vars[1]),
        unchanged(new_behaviour_vars[0], new_behaviour_vars[1])
    )
)

constraints.append(
    If(
        c2_updater_conditions(new_behaviour_vars[1]), 
        c2_updater_transition(new_behaviour_vars[1], new_behaviour_vars[2]),
        unchanged(new_behaviour_vars[1], new_behaviour_vars[2])
    )
)

constraints.append(
    If(
        d_updater_conditions(new_behaviour_vars[2]), 
        d_updater_transition(new_behaviour_vars[2], new_behaviour_vars[3]),
        unchanged(new_behaviour_vars[2], new_behaviour_vars[3])
    )
)

s.add(And(*constraints))

# Ask z3 to find a situation in which at least one
# of the variables in the final states is different
# between the two behaviours
final_old = old_behaviour_vars[3]
final_new = new_behaviour_vars[3]
s.add(
    Or(
        final_old['a'] != final_new['a'],
        final_old['b'] != final_new['b'],
        final_old['c'] != final_new['c'],
        final_old['d'] != final_new['d'],
    )
)
