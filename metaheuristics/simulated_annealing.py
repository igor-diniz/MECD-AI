from metaheuristics.solver import Solver 
from helpers.solution import Solution
from copy import deepcopy
import numpy as np
import random
import time
import tracemalloc

class SimulatedAnnealing(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.initial_solution = super().create_initial_solution(mode="random")
        self.internal_neighbors_generator = super().get_internal_neighbour
        self.external_neighbors_generator = super().get_external_neighbour

    def select_initial_solution_type(self, initial_solution_random, initial_solution_greedy):
        selected_initial_solution = random.choice(["random", "greedy"])
        if selected_initial_solution == "random":
            initial_solution = initial_solution_random
        else: 
            initial_solution = initial_solution_greedy
        return initial_solution

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
   
    def solve(
            self, initial_solution_random,
            initial_solution_greedy,
            internal_neighbors_generator,
            external_neighbors_generator,
            num_iterations: int,
            T: float, 
            cooling_schedule: float,
            log=False
            ):
            
            start_time = time.time()
            tracemalloc.start()
            tracemalloc.clear_traces()

            print("Generating Initial Solution...")

            iteration = 0
            temperature = T
            solution = self.select_initial_solution_type(initial_solution_random,initial_solution_greedy)  # Best solution after 'num_iterations'
            score = self.evaluate_solution(solution)

            best_solution = deepcopy(solution)
            best_score = score

            while iteration < num_iterations:
                temperature *= cooling_schedule
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
                            print("\nBest Neighbour Selected:\n", neighbor_solution)
                            print("\nBest Solution So Far:\n", best_solution)
            end_time = time.time()
            elapsed_time = end_time - start_time
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            print(f"-----\nElapsed time: {elapsed_time} seconds\nPeak memory: {peak_memory} bytes")
            print("\nFinal Solution:\n", best_solution)
            return best_solution              