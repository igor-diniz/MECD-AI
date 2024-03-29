import time
import tracemalloc
from metaheuristics.solver import Solver
from helpers.solution import Solution
from copy import deepcopy
import random
import numpy as np
import heapq
from helpers import utils

class TabuSearchSolver(Solver):
    def __init__(self, total_books: int, libraries: dict, total_days: int):
        super().__init__(total_books, libraries, total_days)
        n_libraries = len(libraries)
        self.tabu_list = np.zeros((n_libraries, n_libraries), dtype=int)
        self.mask_tabu = np.triu(np.ones_like(self.tabu_list, dtype=bool), 1)   # upper triangle of tabu list matrix
        self.curr_sol_history = []


    def append_n_external_neighbours(self, solution: Solution, score_neighbour_swap: heapq, n: int, enable_penalty: bool):
        """Appends n combinations of neighbours from swaps between external libraries 
        that are not in the solution and internal libraries that is in the solution"""

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
            penalty = self.tabu_list[max(lib1_id, lib2_id)][min(lib1_id, lib2_id)] if enable_penalty else 0
            
            length_neighbours_before = len(neighbourhood_swaps)
            neighbourhood_swaps.add(swap_done)

            if len(neighbourhood_swaps) > length_neighbours_before:
                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score + penalty, neighbour_sol, swap_done))

    
    def append_n_internal_neighbours(self, solution: Solution, score_neighbour_swap: heapq, n: int, enable_penalty: bool):
        """Appends n combinations of neighbours from swaps between two internal libraries 
        that are in the solution, that means n permutations of the libraries in the solution"""

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
            penalty = self.tabu_list[max(lib1_id, lib2_id)][min(lib1_id, lib2_id)] if enable_penalty else 0
            
            length_neighbours_before = len(neighbourhood_swaps)
            neighbourhood_swaps.add(swap_done)
            neighbourhood_swaps.add((swap_done[1], swap_done[0]))

            if len(neighbourhood_swaps) > length_neighbours_before:
                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score + penalty, neighbour_sol, swap_done))


    def append_all_external_neighbours(self, curr_solution: Solution, score_neighbour_swap: heapq, enable_penalty: bool):
        """Appends all combinations of neighbours from swaps between external libraries 
        that are not in the solution and internal libraries that is in the solution"""
        
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
                penalty = self.tabu_list[max(library_1_id, library_2_id)][min(library_1_id, library_2_id)] if enable_penalty else 0

                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score + penalty, neighbour_sol, swap_done))
    

    def append_all_internal_neighbours(self, curr_solution: Solution, score_neighbour_swap: heapq, enable_penalty: bool):
        """Appends all combinations of neighbours from swaps between two internal libraries 
        that are in the solution, that means all permutations of the libraries in the solution"""
        
        libraries_sol = deepcopy(curr_solution.libraries)

         # swap libraries in use with libraries also in use
        for library_1_index in range(len(libraries_sol)):
            for library_2_index in range(library_1_index + 1, len(libraries_sol)):
                libraries_sol_copy = deepcopy(curr_solution.libraries)
                libraries_sol_copy[library_1_index], libraries_sol_copy[library_2_index] = libraries_sol_copy[library_2_index], libraries_sol_copy[library_1_index]
                neighbour_sol = deepcopy(super().select_library_books(libraries_sol_copy))
                negative_score = -neighbour_sol.evaluate()
                library_1_id = libraries_sol_copy[library_1_index].id
                library_2_id = libraries_sol_copy[library_2_index].id
                swap_done = (library_1_id, library_2_id)
                penalty = self.tabu_list[max(library_1_id, library_2_id)][min(library_1_id, library_2_id)] if enable_penalty else 0
                
                # add neighbour in the priority queue in the correct place
                heapq.heappush(score_neighbour_swap, (negative_score + penalty, neighbour_sol, swap_done))
    
    
    def get_candidate_list(self, curr_solution: Solution, n: int=None, enable_penalty: bool=False):
        """Gets the candidate list of neighbours as priority queue ordered by the score.
        The priority queue is composed by the score, by the solution itself and the swap done"""
        
        score_neighbour_swap = []   # list of tuples like (diff_score, neighbour_sol, swap_done)
        heapq.heapify(score_neighbour_swap)     # priority queue based on the diff_score
        
        if n is None or n == -1:
            self.append_all_external_neighbours(curr_solution, score_neighbour_swap, enable_penalty)
            self.append_all_internal_neighbours(curr_solution, score_neighbour_swap, enable_penalty)

        else:
            self.append_n_external_neighbours(curr_solution, score_neighbour_swap, int(n*0.7), enable_penalty)
            self.append_n_internal_neighbours(curr_solution, score_neighbour_swap, int(n*0.3), enable_penalty)

        return score_neighbour_swap
    

    def aspiration_criterion_met(self, best_score, new_score):
        """Verifies if the new score from the neighbour is the best reached so far"""
        return best_score < new_score
    
    
    def is_swap_tabu(self, swaped_libs):
        """Verifies if the swap is tabu in the tabu list"""
        min_from_swap = min(swaped_libs)
        max_from_swap = max(swaped_libs)
        return self.tabu_list[min_from_swap][max_from_swap] > 0
    

    def update_tabu_list(self, swaped_libs, tabu_tenure):
        """Sets the tabu tenure for the new swap 
        and updates the long term memory"""
        min_from_swap = min(swaped_libs)
        max_from_swap = max(swaped_libs)
        self.tabu_list[self.mask_tabu & (self.tabu_list != 0)] -= 1         # update tabu frequency of previous swaps
        self.tabu_list[min_from_swap][max_from_swap] = tabu_tenure          # update tabu frequency of current swap
        self.tabu_list[max_from_swap][min_from_swap] += 1                   # update frequency based long term memory


    def solve(self,
              initial_solution: Solution,
              tabu_tenure: int=7,
              n_neighbours: int=None,
              max_iterations: int=1000,
              log: bool=False,
              results_csv: str=None,
              solution_id: str=None,
              filename: str=None,
              timeout: int=3600
              ):
        
        start_time = time.time()
        tracemalloc.start()
        tracemalloc.clear_traces()
        
        best_solution = deepcopy(initial_solution)
        best_score = initial_solution.evaluate()
        curr_solution = deepcopy(initial_solution)
        same_best_sol_times = 0
        enable_penalty = False
        
        self.curr_sol_history.clear()
        self.curr_sol_history.append(best_score)
        
        # number of iterations is one of the stop criterions
        for _ in range(max_iterations):

            # enables the usage of the long term memory
            if same_best_sol_times > tabu_tenure:
                enable_penalty = True

            candidate_list = self.get_candidate_list(curr_solution, n_neighbours, enable_penalty)

            # gets the best neighbour that is not a tabu
            while candidate_list:
                negative_score, best_neighbour, swaped_libs = heapq.heappop(candidate_list)     # get the best neighbour using the heap sctructure
                penalty = self.tabu_list[max(swaped_libs)][min(swaped_libs)] if enable_penalty else 0
                new_score = -(negative_score - penalty)

                # if not a tabu or aspiration criterion met
                if self.aspiration_criterion_met(best_score, new_score) or not self.is_swap_tabu(swaped_libs):
                    curr_solution = best_neighbour
                    self.curr_sol_history.append(new_score)
                    
                    # updates best solution found so far
                    if self.aspiration_criterion_met(best_score, new_score):
                        best_solution = deepcopy(curr_solution)
                        best_score = new_score
                        same_best_sol_times = 0

                    same_best_sol_times += 1
                    
                    self.update_tabu_list(swaped_libs, tabu_tenure)

                    if log:
                        print(f"\nSwap: {swaped_libs}")
                        print("\nBest Neighbour Selected:\n", best_neighbour)
                        print("\nBest Solution So Far:\n", best_solution)
                    break
            
            # all neighbours are tabu, so stop
            if not candidate_list:
                break
            
            # timeout reached, stop
            if time.time() - start_time > timeout:
                break

        end_time = time.time()
        elapsed_time = end_time - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if results_csv and filename:
            utils.results_to_csv(results_csv, self.curr_sol_history, solution_id, filename, best_score, elapsed_time, peak_memory, tabu_tenure, n_neighbours, max_iterations)
            print(f"Result written to {results_csv}.")

        print(f"-----\nElapsed time: {elapsed_time} seconds\nPeak memory: {peak_memory} bytes")
        
        return best_solution
