from metaheuristics.solver import Solver 
from helpers.solution import Solution
from copy import deepcopy
import numpy as np
import random

class SimulatedAnnealing(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.initial_solution = super().create_initial_solution(mode="random")
        self.internal_neighbors_generator = super().get_internal_neighbour

    def evaluate_solution(self, solution):
        total_score = solution.evaluate()
        return total_score

    def solve(self, initial_solution, neighbor_generator, num_iterations: int, log=False):
            iteration = 0
            temperature = 1000
            solution = initial_solution  # Best solution after 'num_iterations'
            score = self.evaluate_solution(solution)

            best_solution = deepcopy(solution)
            best_score = score

            while iteration < num_iterations:
                temperature *= 0.999  # Test with different cooling schedules
                iteration += 1
                neighbor_solution = neighbor_generator(best_solution, "swap")  # Test with internal and external neighbor
                neighbor_score = self.evaluate_solution(neighbor_solution)

                delta = neighbor_score - score

                if delta > 0 or np.exp(-delta / temperature) > random.random():
                    solution = neighbor_solution
                    score = neighbor_score
                    if score > best_score:
                        iteration = 0
                        best_solution = deepcopy(solution)
                        best_score = score
                        if log:
                            print(best_solution)  # Assuming you want to print the best solution when log is True
            return best_solution              