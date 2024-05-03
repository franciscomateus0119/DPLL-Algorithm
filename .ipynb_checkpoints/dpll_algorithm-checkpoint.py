import numpy as np
import copy
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
        #Obtain Clause Set Info
        if 'p' in line:
            clause_set_info = line.split()
            
        if len(line) != 0 and 'c' not in line[0]:
            new_lines = np.append(new_lines, line.rstrip("0"))
    
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

#--------

def get_unique_literals(c_set):
    '''
    For a given clause set, get every literal.
    Return all unique literals
    '''
    literals = np.asarray([])
    for line in c_set:
        for literal in line:
            if literal not in literals:
                literals = np.append(literals, literal)
    return literals

def get_literal(c_set):
    '''
    Searches for the first literal.
    Return the found literal.
    '''
    return c_set[0][0]

def search_unitary_clause_literal(c_set):
    '''
    Searches for a unit clause, containing a single literal.
    Return if found, otherwise Return None.
    '''
    if any(c_set):
        for line in c_set:
            if len(line) == 1:
                return line[0]
    return None

def propagate(c_set):
    literal = search_unitary_clause_literal(c_set)
    if not literal:
        return c_set
    updated_set = c_set
    while literal:
        new_set = []
        for line in updated_set:
                if literal not in line: #Literal não está na cláusula, procurar por cláusulas para remoção
                    if '-' in literal: #Literal contém negação
                        aux_literal = literal.replace('-','') #Remover negação do literal
                        if aux_literal in line: #Se o literal sem negação estiver na linha
                            #print(line)
                            new_line = line
                            new_line.remove(aux_literal) #Remove o literal sem negação da linha, adicionar linha
                            new_set.append(new_line)
                        else: #Literal sem negação também não está na linha
                            new_set.append(line) #Adiciona a linha sem modificações
                    else: #Literal não contém negação
                        aux_literal = '-' + literal #Adiciona a negação ao literal
                        if aux_literal in line: #Se o literal com negação estiver na linha
                            new_line = line
                            new_line.remove(aux_literal) #Remove o literal com negação na linha, adiciona linha
                            new_set.append(new_line)   
                        else: #Literal com negação também não está na linha
                            new_set.append(line) #Adiciona a linha sem modificações
                           
        updated_set = new_set
        literal = search_unitary_clause_literal(new_set)
    return updated_set      

def dpll(clause_set):
    returned_set = propagate(copy.deepcopy(clause_set))
    if len(returned_set) == 0:
        return True
    if not all(returned_set):
        return False
    chosen_literal = get_literal(returned_set)
    neg_chosen_literal = None
    if '-' in chosen_literal:
        neg_chosen_literal = chosen_literal.replace('-','')
    else:
        neg_chosen_literal = '-' + chosen_literal
    clause_set_and_chosen_literal = copy.deepcopy(returned_set)
    clause_set_and_chosen_literal.append([chosen_literal])
    if dpll(clause_set_and_chosen_literal):
        return True
    else:
        clause_set_and_chosen_literal[-1] = [neg_chosen_literal]
        return dpll(clause_set_and_chosen_literal)       
        
def dpll_read_file(file_path):
    clauses, clause_set_info = read_given_file(file_path)
    return dpll(clauses)