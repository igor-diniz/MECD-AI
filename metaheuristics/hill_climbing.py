from metaheuristics.solver import Solver 
from helpers.solution import Solution
from copy import deepcopy
import random

class HillClimbingSolver(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.initial_solution = super().create_initial_solution(mode="random")
        self.neighbors_generator = super().get_internal_neighbour

    def evaluate_solution(self, solution):
        total_score = solution.evaluate()
        return total_score

    def solve(self, initial_solution,neighbors_generator, max_iterations=1000):
        x = initial_solution
        actual_score = self.evaluate_solution(x)
        for _ in range(max_iterations):
            neighbors = neighbors_generator(x, "swap")
            neighbor_score = self.evaluate_solution(neighbors)
            if neighbor_score > actual_score:
                x = neighbors
            return x  # Return the best solution found within the maximum iterations

