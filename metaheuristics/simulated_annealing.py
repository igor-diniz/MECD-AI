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
        self.external_neighbors_generator = super().get_external_neighbour

    def evaluate_solution(self, solution):
        total_score = solution.evaluate()
        return total_score
   
    def select_neighbor_generator(self, solution: Solution, internal_neighbors_generator, external_neighbors_generator):
        choice = ["internal", "external"]
        selected_generator = random.choice(choice)
        if selected_generator == "external":
            neighbor_generator = external_neighbors_generator(solution)
        else: 
            neighbor_generator = internal_neighbors_generator(solution, "swap")
        return  neighbor_generator   
   
    def solve(self, initial_solution, internal_neighbors_generator, external_neighbors_generator, num_iterations: int, log=False):
            iteration = 0
            temperature = 1000
            solution = initial_solution  # Best solution after 'num_iterations'
            score = self.evaluate_solution(solution)

            best_solution = deepcopy(solution)
            best_score = score

            while iteration < num_iterations:
                temperature *= 0.999  # Test with different cooling schedules
                iteration += 1
                neighbor_solution = self.select_neighbor_generator(solution, internal_neighbors_generator, external_neighbors_generator) 
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
                            print(f"Solution:       {best_solution}, score: {best_score}")
            print(f"Final Solution: {best_solution}, score: {best_score}")
            return best_solution              