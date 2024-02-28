from metaheuristics.solver import Solver 
from helpers.solution import Solution
from copy import deepcopy
import numpy as np
from helpers.utils import results_to_csv
import random
import time
import tracemalloc

class SimulatedAnnealing(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.curr_sol_history = []

    def evaluate_solution(self, solution):
        total_score = solution.evaluate()
        return total_score
   
    def select_neighbor_generator(self, solution: Solution):
        selected_generator = random.choice(["internal", "external"])
        if selected_generator == "external":
            neighbor_generator = self.get_external_neighbour(solution)
        else: 
            neighbor_generator = self.get_internal_neighbour(solution, "swap")
        return  neighbor_generator   
   
    def solve(
            self, initial_solution,
            num_iterations: int,
            T: float, 
            cooling_schedule: float,
            log=False,
            results_csv = None,
            filename = None
            ):
            
            start_time = time.time()
            tracemalloc.start()
            tracemalloc.clear_traces()

            print("Generating Initial Solution...")

            iteration = 0
            temperature = T
            solution = initial_solution
            score = self.evaluate_solution(solution)

            best_solution = deepcopy(solution)
            best_score = score

            while iteration < num_iterations:
                temperature *= cooling_schedule
                iteration += 1
                neighbor_solution = self.select_neighbor_generator(best_solution)
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

            if results_csv and filename:
                results_to_csv(results_csv, filename, best_solution, score, elapsed_time, peak_memory)
                print(f"Result written to {results_csv}.")

            print(f"-----\nElapsed time: {elapsed_time} seconds\nPeak memory: {peak_memory} bytes")
            print("\nFinal Solution:\n", best_solution)
            return best_solution              