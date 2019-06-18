from z3 import *

# We'll have two variables, `a` and `b`. We need to define
# distinct Z3 variables for each of those, for each point in time
# If we have two Meander rules, it means a ticket will go through
# three points in time:
#    1. The initial time (t=0), when we receive a ticket update or ticket creation event
#    2. The second point in time (t=1), when the ticket has passed through rule 1
#    3. The third point in time (t=2), when the ticket has passed through rule 2

# The different states represent the state of the variables at time t
# So states[0] is the values of `a` and `b` at t=0
states = {
    # The start of time, i.e. "the ticket fields right before
    # we run the first rule"
    0: {
        'a': Int('a_0'),
        'b': Int('b_0')
    },

    # The state after the first rule has been run
    1: {
        'a': Int('a_1'),
        'b': Int('b_1')
    },
    
    # The state after the second rule has been run
    2: {
        'a': Int('a_2'),
        'b': Int('b_2')
    },
    
}

s = Solver()

# This is representing 'all the possible values'
# that these variables might have on a new or updated ticket
s.add(states[0]['a'] >= 0, states[0]['a'] <= 10)
s.add(states[0]['b'] >= 0, states[0]['b'] <= 5)

# Condition
#   a > 5
def rule1_condition(state):
    return state['a'] > 5

# Action
#   b := b + 5
def rule1_action(curr_state, next_state):
    return And(
        next_state['b'] == curr_state['b'] + 5,
        next_state['a'] == curr_state['a']
    )

# Condition
#    All of:
#       a > 6
#       b >= 10
def rule2_condition(state):
    return And(
        state['a'] > 6,
        state['b'] >= 10
    )

# Action
#   a := a + b
def rule2_action(curr_state, next_state):
    return And(
        next_state['a'] == curr_state['a'] + curr_state['b'],
        next_state['b'] == curr_state['b']
    )

# Return a constraint that between two states,
# none of our variables change
def unchanged(curr_state, next_state):
    return And(
        next_state['a'] == curr_state['a'],
        next_state['b'] == curr_state['b']
    )


s.add(
    # If rule1 is true in state0, then perform rule1's action
    # Otherwise the variables remain unchanged
    If(
        rule1_condition(states[0]),
        # then
        rule1_action(states[0], states[1]),
        # else
        unchanged(states[0], states[1])
    ) 

)

s.add(
    # If rule2 is true in state1, then perform rule2's action
    # Otherwise the variables remain unchanged
    If(
        rule2_condition(states[1]),
        # then
        rule2_action(states[1], states[2]),
        # else
        unchanged(states[1], states[2])
    ) 

)

# Can any initial combination of `a` and `b` cause
# the chain of rules to end up with a=17?
s.add(states[2]['a'] == 17)