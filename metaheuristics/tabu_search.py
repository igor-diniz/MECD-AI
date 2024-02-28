from metaheuristics.solver import Solver
from helpers.solution import Solution
from copy import deepcopy
import random
import numpy as np
import heapq
import csv
import os

class TabuSearchSolver(Solver):
    def __init__(self, total_books: int, libraries: dict, total_days: int):
        super().__init__(total_books, libraries, total_days)
        n_libraries = len(libraries)
        self.tabu_list = np.zeros((n_libraries, n_libraries), dtype=int)
        self.mask_frequency_based = np.tril(np.ones_like(self.tabu_list, dtype=bool), -1)
        self.mask_tabu = np.triu(np.ones_like(self.tabu_list, dtype=bool), 1)
        self.curr_sol_history = []


    def append_n_external_neighbours(self, solution: Solution, score_neighbour_swap: heapq, n: int):
        neighbourhood_swaps = set()
        n_libraries = len(self.libraries)
        n_sol_libraries = len(solution.libraries)
        sol_libraries_ids = list(map(lambda library: library.id, solution.libraries))
        n_max_neighbours = (n_libraries - n_sol_libraries) * n_sol_libraries

        while len(neighbourhood_swaps) < min(n, n_max_neighbours):
            sol_libraries = deepcopy(solution.libraries)
            sol_libraries_indexes = list(range(len(sol_libraries)))
            
            not_solution_libraries = [library for library in self.libraries.values() if library.id not in sol_libraries_ids]
            not_solution_libraries_indexes = list(range(len(not_solution_libraries)))

            index_1 = random.choice(sol_libraries_indexes)
            index_2 = random.choice(not_solution_libraries_indexes)

            lib1_id = sol_libraries[index_1].id
            lib2_id = not_solution_libraries[index_2].id

            sol_libraries[index_1] = not_solution_libraries[index_2]
            
            neighbour_sol = deepcopy(self.select_library_books(sol_libraries))
            negative_score = -neighbour_sol.evaluate()
            swap_done = (lib1_id, lib2_id)
            
            length_neighbours_before = len(neighbourhood_swaps)
            neighbourhood_swaps.add(swap_done)

            if len(neighbourhood_swaps) > length_neighbours_before:
                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score, neighbour_sol, swap_done))
                #print(swap_done)
                #print(neighbour_sol)

    
    def append_n_internal_neighbours(self, solution: Solution, score_neighbour_swap: heapq, n: int):
        neighbourhood_swaps = set()
        n_sol_libraries = len(solution.libraries)
        n_max_neighbours = n_sol_libraries * (n_sol_libraries - 1)

        while len(neighbourhood_swaps) < min(2 * n, n_max_neighbours):
            sol_libraries = deepcopy(solution.libraries)
            sol_libraries_indexes = list(range(len(sol_libraries)))

            index_1 = random.choice(sol_libraries_indexes)
            sol_libraries_indexes.remove(index_1)
            index_2 = random.choice(sol_libraries_indexes)

            lib1_id = sol_libraries[index_1].id
            lib2_id = sol_libraries[index_2].id

            sol_libraries[index_1], sol_libraries[index_2] = sol_libraries[index_2], sol_libraries[index_1]
            
            neighbour_sol = deepcopy(self.select_library_books(sol_libraries))
            negative_score = -neighbour_sol.evaluate()
            swap_done = (lib1_id, lib2_id)
            
            length_neighbours_before = len(neighbourhood_swaps)
            neighbourhood_swaps.add(swap_done)
            neighbourhood_swaps.add((swap_done[1], swap_done[0]))

            if len(neighbourhood_swaps) > length_neighbours_before:
                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score, neighbour_sol, swap_done))
                #print(swap_done)
                #print(neighbour_sol)


    def append_all_external_neighbours(self, curr_solution: Solution, score_neighbour_swap: heapq):
        libraries_sol = deepcopy(curr_solution.libraries)

        # get libraries not in the current solution
        libraries_not_included = deepcopy(self.libraries)
        for library in libraries_sol:
            libraries_not_included.pop(library.id)

        # swap libraries in use with libraries not in use
        for library_1_index in range(len(libraries_sol)):
            for library_2_id in libraries_not_included:
                library_1_id = libraries_sol[library_1_index].id
                libraries_sol_copy = deepcopy(curr_solution.libraries)
                libraries_sol_copy[library_1_index] = libraries_not_included[library_2_id]
                neighbour_sol = deepcopy(super().select_library_books(libraries_sol_copy))
                negative_score = -neighbour_sol.evaluate()
                swap_done = (library_1_id, library_2_id)

                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score, neighbour_sol, swap_done))
    

    def append_all_internal_neighbours(self, curr_solution: Solution, score_neighbour_swap: heapq):
        libraries_sol = deepcopy(curr_solution.libraries)

         # swap libraries in use with libraries also in use
        for library_1_index in range(len(libraries_sol)):
            for library_2_index in range(library_1_index + 1, len(libraries_sol)):
                libraries_sol_copy = deepcopy(curr_solution.libraries)
                libraries_sol_copy[library_1_index], libraries_sol_copy[library_2_index] = libraries_sol_copy[library_2_index], libraries_sol_copy[library_1_index]
                neighbour_sol = deepcopy(super().select_library_books(libraries_sol_copy))
                negative_score = -neighbour_sol.evaluate()
                swap_done = (libraries_sol_copy[library_1_index].id, libraries_sol_copy[library_2_index].id)
                
                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score, neighbour_sol, swap_done))
    
    
    def get_candidate_list(self, curr_solution: Solution, n: int=None):
        score_neighbour_swap = []   # list of tuples like (diff_score, neighbour_sol, swap_done)
        heapq.heapify(score_neighbour_swap)     # priority queue based on the diff_score
        
        if n is None or n == -1:
            self.append_all_external_neighbours(curr_solution, score_neighbour_swap)
            self.append_all_internal_neighbours(curr_solution, score_neighbour_swap)

        else:
            self.append_n_external_neighbours(curr_solution, score_neighbour_swap, n//2)
            self.append_n_internal_neighbours(curr_solution, score_neighbour_swap, n//2)

        return score_neighbour_swap
    

    def acceptance_criterion_met(self, best_score, new_score):
        return best_score < new_score
    
    
    def is_swap_tabu(self, swaped_libs):
        min_from_swap = min(swaped_libs)
        max_from_swap = max(swaped_libs)
        return self.tabu_list[min_from_swap][max_from_swap] > 0
    

    def update_tabu_list(self, swaped_libs, tabu_tenure):
        min_from_swap = min(swaped_libs)
        max_from_swap = max(swaped_libs)
        self.tabu_list[self.mask_tabu & (self.tabu_list != 0)] -= 1         # update tabu frequency of previous swaps
        self.tabu_list[min_from_swap][max_from_swap] = tabu_tenure          # update tabu frequency of current swap
        self.tabu_list[max_from_swap][min_from_swap] += 1                   # update frequency based long term memory


    def solve(self, initial_solution: Solution, tabu_tenure: int=7, n_neighbours: int=None, max_iterations: int=1000, log: bool=False, filename: str=None):
        best_solution = deepcopy(initial_solution)
        best_score = initial_solution.evaluate()
        curr_solution = deepcopy(initial_solution)
        
        self.curr_sol_history.clear()
        self.curr_sol_history.append(best_score)
        
        for _ in range(max_iterations):
            candidate_list = self.get_candidate_list(curr_solution, n_neighbours)

            while candidate_list:
                negative_score, best_neighbour, swaped_libs = heapq.heappop(candidate_list)     # get the best neighbour using the heap sctructure
                new_score = -negative_score

                # if not a tabu or acceptance criterion met
                if self.acceptance_criterion_met(best_score, new_score) or not self.is_swap_tabu(swaped_libs):
                    curr_solution = best_neighbour
                    self.curr_sol_history.append(new_score)
                    
                    if self.acceptance_criterion_met(best_score, new_score):
                        best_solution = deepcopy(curr_solution)
                        best_score = new_score
                    
                    self.update_tabu_list(swaped_libs, tabu_tenure)

                    if log:
                        print(f"\nSwap: {swaped_libs}")
                        print("\nBest Neighbour Selected:\n", best_neighbour)
                        print("\nBest Solution So Far:\n", best_solution)
                    break
            
            if not candidate_list:
                break
        
        return best_solution
    

    def save_metrics(self, file_name_instance, initial_solution_score, initial_time, initial_memory, initial_type,
                            tabu_solution_score, tabu_time, tabu_memory,
                            tabu_tenure, n_neighbours_per_iteration, max_iterations):
        
        file_name = "analysis/ts/metrics.csv"
        # Create or append to the CSV file
        with open(file_name, mode='a+' if os.path.exists(file_name) else 'w+', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If file is empty, write header
                writer.writerow(["ID", "File Instance", "Initial Score", "Initial Time", "Initial Memory", "Initial Type",
                                "Tabu Score", "Tabu Time", "Tabu Memory",
                                "Tabu Tenure", "Candidate List Size", "Max Iterations"])

            file.seek(0)
            rows = file.readlines()

            if len(rows) > 1:  # Check if there is more than just the header row
                last_row = rows[-1]
                last_row = int(last_row[0]) + 1
            else: 
                last_row = 1

            # Write the results to the CSV file
            writer.writerow([last_row, file_name_instance, initial_solution_score, initial_time, initial_memory, initial_type,
                            tabu_solution_score, tabu_time, tabu_memory,
                            tabu_tenure, n_neighbours_per_iteration, max_iterations])
            
        self.save_history(last_row)
            
    
    def save_history(self, id):
        # Create or append to the CSV file
        file_name = "analysis/ts/solutions_history.csv"
        with open(file_name, mode='a' if os.path.exists(file_name) else 'w', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # If file is empty, write header
                writer.writerow(["ID", "Solution History"])

            # Write the solution history to the CSV file
            for solution_score in self.curr_sol_history:
                writer.writerow([id, solution_score])          



