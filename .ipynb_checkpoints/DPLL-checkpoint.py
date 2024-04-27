import numpy as np
import copy
from functions import *   

def dpll(clause_set):
    '''
    DPLL Algorithm
    
    1. Run propagate(clause set) for a given clause set.
    2. Get the propagate resulting clause set
    2.1 Early Stop and
        -Return True if the clause set is empty
        -Return False if the clause set contains an empty clause
    3 Chose a literal using a chosen strategy (random in this case)
    4 Run DPLL recursively with an updated clause set
        -Clause set + Literal. Return True.
        -Clause set + Negated Literal. Return recursive result.
        
    Return True -> SAT, Return False -> Unsat
    Note: This algorithm does not check for Unknown.
    '''
    clause_set = propagate(copy.deepcopy(clause_set))
    # Stopping conditions
    # Returned set is empty -> []
    if len(clause_set) == 0:
        return True
    # Returned set if an empty clause -> [[]]
    if len(clause_set) == 1 and len(clause_set[0]) == 0:
        return False
    # Choose a random literal
    chosen_literal = np.random.choice(get_unique_literals(clause_set))
    # Add chosen literal as a unit literal clause and run dpll recursively
    if dpll(copy.deepcopy(clause_set) + [chosen_literal]):
        return True
    # Add negated chosen literal as a unit literal clause and run dpll recursively
    else:
        return dpll(copy.deepcopy(clause_set) + [chosen_literal])