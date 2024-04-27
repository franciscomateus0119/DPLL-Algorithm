import numpy as np
def read_given_file(file_path):
    '''
    Opens a File in DIMACS CNF format.
    Obtain the CNF information.
    Obtain each clause (line), creating the clause set.
    Return the clause set and CNF information.
    '''
    # Opening file
    file = open(file_path, 'r')

    # Get Clauses
    lines =  np.asarray([line.rstrip() for line in file])
    
    # Closing files
    file.close()
    
    new_lines = np.array([])
    for i,line in enumerate(lines):
        if 'c' not in line[0]:
            new_lines = np.append(new_lines, line.replace("0",""))
    #Obtain Clause Set Info
    clause_set_info = new_lines[0].split()    
    
    #Obtain Clauses
    clauses = get_split_clauses(new_lines[1:])

    return clauses, clause_set_info

def get_split_clauses(c_set):
    '''
    For a given clause set in CNF format, separate the literals in each clause.
    Every '^' (' ' in DIMACS CNF) becomes a ',' such that [1,2,..,n] is a clause
    of n literal separated by '.
    
    Return the modified clause set.
    '''
    new_c_set = []
    for line in c_set:
        new_c_set.append(line.split())
    return new_c_set

def get_unique_literals(c_set):
    '''
    For a given clause set, get every literal.
    Return all unique literals
    '''
    literals = []
    for line in c_set[0]:
        negative = False
        for char in line.split():
            if negative:
                literals.append('-'+char)
            else:
                literals.append(char)
    return np.unique(literals)



def check_line_literal(c_set):
    '''
    For a given clause set, search for an unit literal in each line
    
    Return True, literal if an unit literal has been found
    Return False, None if an unit literal has not been found
    '''
    for line in c_set:
        if len(line) == 1:
            if line[0].count('-') >= 2:
                if line[0].count('-') % 2 == 0:
                    return True, line[0].replace('-','')
                else:
                    return True, '-' + line[0].replace('-','')
            return True, line[0]
    return False, None

def propagate(c_set):
    '''
    For a given clause set, follow the steps:
    1. Search for a unit literal.
    1.1 If a literal has not been found, Return the current set.
    
    2. Repeat the following steps while a unit literal is being found
    2.1 Remove clause set lines which contains the unit literal
    2.2 Eliminate clause set lines which contains unit negated literal
    2.3 Search for a new unit literal
    
    3. Return the resulting clause set
    '''
    check_literal, literal = check_line_literal(c_set)
    if not check_literal:
        return c_set
    #While there is a unit clause
    while literal:        
        new_set = []
        for line in c_set:
            # Checks if literal not in line
            if literal not in line:
                # Checks if neg literal
                if '-' not in literal:
                    # Remove neg literal from line if literal = True, add line
                    if '-'+literal in line:
                        line.remove('-'+literal)
                        new_set.append(line)
                    #  Neg literal not in line, Add line
                    else:
                        new_set.append(line)
                # Neg literal in line
                else:
                    if literal.replace('-','') in line:
                        line.remove(literal.replace('-',''))
                        new_set.append(line)
                    else:
                        new_set.append(line)
        c_set = new_set        
        check_literal, literal = check_line_literal(c_set)        
    return c_set