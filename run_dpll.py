import numpy as np
import argparse
import time
from dpll_algorithm import *

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="cnf file input path",)
args = parser.parse_args()
clauses, clause_set_info = read_given_file(args.input)
print(f'Found Info: {clause_set_info}')
print(dpll(clauses))


