from metaheuristics.solver import Solver 
from helpers.solution import Solution
from copy import deepcopy
from helpers.utils import results_to_csv
import random
import time
import tracemalloc

class HillClimbingSolver(Solver):
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
            log=False,
            results_csv=None,
            solution_id: str=None,
            filename=None,
            timeout: int=3600
            ):
        
        start_time = time.time()
        tracemalloc.start()
        tracemalloc.clear_traces()

        print("Generating Initial Solution...")

        iteration = 0
        best_solution = initial_solution
        actual_score = self.evaluate_solution(best_solution)

        print(f"Init Solution:  {best_solution}, score: {actual_score}")
        
        while iteration < num_iterations and time.time() - start_time < timeout:
            iteration += 1
            neighbors_solution =  self.select_neighbor_generator(best_solution)
            neighbor_score = self.evaluate_solution(neighbors_solution)
            
            if neighbor_score > actual_score:
                best_solution = neighbors_solution
                actual_score = neighbor_score

                if log: 
                    print("\nBest Neighbour Selected:\n", neighbors_solution)
                    print("\nBest Solution So Far:\n", best_solution)
            
            self.curr_sol_history.append(actual_score)
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if results_csv and filename:
            results_to_csv(results_csv, self.curr_sol_history, solution_id, filename, actual_score, elapsed_time, peak_memory, num_iterations)
            print(f"Result written to {results_csv}.")

        print(f"-----\nElapsed time: {elapsed_time} seconds\nPeak memory: {peak_memory} bytes")
        print("\nFinal Solution:\n", best_solution)
        return best_solution  # Return the best solution found within the maximum iterations
            
