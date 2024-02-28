from metaheuristics.solver import Solver 
from helpers.solution import Solution
from copy import deepcopy
import random
import time
import tracemalloc

class HillClimbingSolver(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.initial_solution_random = super().create_initial_solution(mode="random")
        self.initial_solution_greedy = super().create_initial_solution(mode="greedy")
        self.internal_neighbors_generator = super().get_internal_neighbour
        self.external_neighbors_generator = super().get_external_neighbour

    def evaluate_solution(self, solution):
        total_score = solution.evaluate()
        return total_score
    
    def select_neighbor_generator(self, solution: Solution, internal_neighbors_generator, external_neighbors_generator):
        selected_generator = random.choice(["internal", "external"])
        if selected_generator == "external":
            neighbor_generator = external_neighbors_generator(solution)
        else: 
            neighbor_generator = internal_neighbors_generator(solution, "swap")
        return  neighbor_generator
    
    def select_initial_solution_type(self, initial_solution_random, initial_solution_greedy):
        selected_initial_solution = random.choice(["random", "greedy"])
        if selected_initial_solution == "random":
            initial_solution = initial_solution_random
        else: 
            initial_solution = initial_solution_greedy
        return initial_solution        

    def solve(
            self, initial_solution_random,
            initial_solution_greedy,
            internal_neighbors_generator,
            external_neighbors_generator,
            num_iterations: int,
            log = False
            ):
        
        start_time = time.time()
        tracemalloc.start()
        tracemalloc.clear_traces()

        print("Generating Initial Solution...")

        iteration = 0
        best_solution = self.select_initial_solution_type(initial_solution_random, initial_solution_greedy)
        actual_score = self.evaluate_solution(best_solution)

        print(f"Init Solution:  {best_solution}, score: {actual_score}")
        
        while iteration < num_iterations:
            iteration += 1
            neighbors_solution = self.select_neighbor_generator(best_solution, internal_neighbors_generator, external_neighbors_generator) 
            neighbor_score = self.evaluate_solution(neighbors_solution)
            if neighbor_score > actual_score:
                iteration = 0
                best_solution = neighbors_solution
                actual_score = neighbor_score
                if log: 
                    print("\nBest Neighbour Selected:\n", neighbors_solution)
                    print("\nBest Solution So Far:\n", best_solution)
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"-----\nElapsed time: {elapsed_time} seconds\nPeak memory: {peak_memory} bytes")
        print("\nFinal Solution:\n", best_solution)
        return best_solution  # Return the best solution found within the maximum iterations
            
