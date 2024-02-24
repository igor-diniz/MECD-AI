from metaheuristics.solver import Solver
from helpers.solution import Solution
from copy import deepcopy
import random

class TabuSearchSolver(Solver):
    def __init__(self, total_books, libraries, total_days, tabu_tenure):
        super().__init__(total_books, libraries, total_days)
        self.tabu_tenure = tabu_tenure

    def solve(self):
        return None
