from helpers.solution import Solution
from copy import deepcopy
import random
import numpy as np

class Solver:
    def __init__(self, total_books, libraries, total_days):
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days 

    def create_initial_solution(self, mode: str):
        remaining_days = self.total_days
        initial_solution = deepcopy(Solution())
        libraries_list = list(self.libraries.values())
        while remaining_days > 0 and libraries_list:
            library = self.__select_library(libraries_list, mode)
            libraries_list.remove(library)    # To avoid select the same library again
            remaining_days -= library.signup_days
            if remaining_days > 0:
                initial_solution.add_library(library)

            next_book_id = 0
            n_books_scanned = 0
            len_book_list = len(library.book_list)

            while next_book_id < len_book_list and \
                n_books_scanned <= remaining_days * library.ship_per_day:

                book_max_score = library.book_list[next_book_id]
                scanned = initial_solution.add_book(book_max_score)
                
                if scanned:
                    book_max_score.library_id = library.id
                    n_books_scanned += 1
                
                next_book_id += 1
        
        return initial_solution
    
    def __select_library(self, libraries_list, mode):
        if mode.lower() == "greedy":
            return max(libraries_list, key=lambda library: (library.total_score * library.ship_per_day) / library.signup_days)
        # if not greedy, select randomly
        return random.choice(libraries_list)
 
    def get_internal_neighbour(self, solution: Solution, mode: str):
        copy_solution = deepcopy(solution)
        sol_libraries = deepcopy(copy_solution.libraries)
        n_libraries = list(range(0, len(sol_libraries)))
        index_1 = random.choice(n_libraries)

        if mode.lower() == "swap":    
            n_libraries.remove(index_1)
            index_2 = random.choice(n_libraries)
            sol_libraries[index_1], sol_libraries[index_2] = sol_libraries[index_2], sol_libraries[index_1]
        else:
            sol_libraries.remove(sol_libraries[index_1])

        return self.select_library_books(sol_libraries)
    
    def get_external_neighbour(self, solution: Solution):
        
        copy_solution = deepcopy(solution)

        internal_libraries = deepcopy(copy_solution.libraries)
        n_libraries_internal = list(range(0, len(internal_libraries)))
        
        external_libraries = [library for library in self.libraries.values() if library not in internal_libraries]
        n_libraries_external = list(range(0, len(external_libraries)))

        index_1 = random.choice(n_libraries_internal)
        index_2 = random.choice(n_libraries_external)

        internal_libraries[index_1] = external_libraries[index_2]
           
        return self.select_library_books(internal_libraries)  

    def select_library_books(self, libraries_list: list):
        libraries_list = deepcopy(libraries_list)
        updated_solution = deepcopy(Solution())
        remaining_days = self.total_days
        
        for library in libraries_list:
            remaining_days -= library.signup_days
            next_book_id = 0
            n_books_scanned = 0

            if remaining_days > 0:
                updated_solution.add_library(library)
            
            len_book_list = len(library.book_list)
            while next_book_id < len_book_list and \
                n_books_scanned <= remaining_days * library.ship_per_day:
                book_max_score = library.book_list[next_book_id]
                scanned = updated_solution.add_book(book_max_score)
                
                if scanned:
                    book_max_score.library_id = library.id
                    n_books_scanned += 1
                
                next_book_id += 1
        
        return updated_solution

    def clear(self):
        for library in self.libraries.values():
            library.reset()
            for book in library.book_list:
                book.reset()
        
    def solve(self):
        # WIP
        return None
