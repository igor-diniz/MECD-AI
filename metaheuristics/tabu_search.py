from metaheuristics.solver import Solver
from helpers.solution import Solution
from copy import deepcopy
import random
import numpy as np
import heapq

class TabuSearchSolver(Solver):
    def __init__(self, total_books: int, libraries: dict, total_days: int, tabu_tenure: int, max_iterations: int=1000):
        super().__init__(total_books, libraries, total_days)
        n_libraries = len(libraries)
        self.tabu_tenure = tabu_tenure
        self.tabu_list = np.zeros((n_libraries, n_libraries), dtype=int)
        self.mask_frequency_based = np.tril(np.ones_like(self.tabu_list, dtype=bool), -1)
        self.mask_tabu = np.triu(np.ones_like(self.tabu_list, dtype=bool), 1)
        self.max_iterations = max_iterations


    def get_candidate_list(self, curr_solution: Solution):
        libraries_sol = deepcopy(curr_solution.libraries)
        diffscore_neighbour_swap = []   # list of tuples like (diff_score, neighbour_sol, swap_done)
        heapq.heapify(diffscore_neighbour_swap)     # priority queue based on the diff_score

        libraries_not_included = deepcopy(self.libraries)
        # remove libraries in the current solution
        for library in libraries_sol:
            libraries_not_included.pop(library.id)

        # swap libraries in use with libraries not in use
        for library_1_index in range(len(libraries_sol)):
            for library_2_id in libraries_not_included:
                library_1_id = libraries_sol[library_1_index].id
                libraries_sol_copy = deepcopy(curr_solution.libraries)
                libraries_sol_copy[library_1_index] = libraries_not_included[library_2_id]
                neighbour_sol = deepcopy(super().select_library_books(libraries_sol_copy))
                print(neighbour_sol)
                diff_score = curr_solution.evaluate() - neighbour_sol.evaluate()
                swap_done = (library_1_id, library_2_id)

                heapq.heappush(diffscore_neighbour_swap, (diff_score, neighbour_sol, swap_done))

        # swap libraries in use with libraries also in use
        for library_1_index in range(len(libraries_sol)):
            for library_2_index in range(library_1_index + 1, len(libraries_sol)):
                libraries_sol_copy = deepcopy(curr_solution.libraries)
                libraries_sol_copy[library_1_index], libraries_sol_copy[library_2_index] = libraries_sol_copy[library_2_index], libraries_sol_copy[library_1_index]
                neighbour_sol = deepcopy(super().select_library_books(libraries_sol_copy))
                print(neighbour_sol)
                diff_score = curr_solution.evaluate() - neighbour_sol.evaluate()
                swap_done = (libraries_sol_copy[library_1_index].id, libraries_sol_copy[library_2_index].id)

                heapq.heappush(diffscore_neighbour_swap, (diff_score, neighbour_sol, swap_done))
        
        return diffscore_neighbour_swap
    

    def solve(self, initial_solution: Solution):
        best_solution = deepcopy(initial_solution)
        best_score = initial_solution.evaluate()
        curr_solution = deepcopy(initial_solution)
        
        for i in range(self.max_iterations):
            print("iteration:", i)
            candidate_list = self.get_candidate_list(curr_solution)
            #print()
            #print("candidate_list:", candidate_list)

            while candidate_list:
                diff_score, best_neighbour, swaped_libs = heapq.heappop(candidate_list)     # get the best neighbour using the heap sctructure
                #print(diff_score)
                #print("BEST NEIGHBOUR:\n", best_neighbour)
                #print("BEST NEIGHBOUR SCORE:", best_neighbour.evaluate())

                # not a tabu or acceptance criterion met
                if diff_score < 0 or self.tabu_list[swaped_libs[0]][swaped_libs[1]] == 0:
                    print("BEST NEIGHBOUR SELECTED:\n", best_neighbour)
                    print("BEST NEIGHBOUR SELECTED SCORE:", best_neighbour.evaluate())
                    print()               
                    curr_solution = best_neighbour
                    
                    if diff_score < 0:
                        best_solution = deepcopy(curr_solution)
                        best_score -= diff_score

                    # update tabu list
                    min_from_swap = min(swaped_libs)
                    max_from_swap = max(swaped_libs)
                    self.tabu_list[self.mask_tabu & (self.tabu_list != 0)] -= 1         # update tabu frequency of previous swaps
                    self.tabu_list[min_from_swap][max_from_swap] = self.tabu_tenure     # update tabu frequency of current swap
                    self.tabu_list[max_from_swap][min_from_swap] += 1                   # update frequency based long term memory
                    break
            
            if not candidate_list:
                break

        return best_solution
                    




