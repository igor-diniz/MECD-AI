from helpers.solution import Solution
from copy import deepcopy
import random

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
    
    def select_library_books(self, solution: Solution):
        deepcopy_sol = deepcopy(solution)
        libraries_list = deepcopy_sol.libraries
        updated_solution = Solution()
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

    def __select_library(self, libraries_list, mode):
        if mode.lower() == "greedy":
            return max(libraries_list, key=lambda library: (library.total_score * library.ship_per_day) / library.signup_days)
        # if not greedy, select randomly
        return random.choice(libraries_list)
    
    def clear(self):
        for library in self.libraries.values():
            library.reset()
            
            for book in library.book_list:
                book.reset()
        
    def solve(self):
        # WIP
        return None

class GenericAlgorithm(Solver):
    def __init__(self):
        super().__init__()
    
    def generate_population(self, population_size):
        parent_solver =  Solver(self.total_books, self.libraries, self.total_days)
        solutions = []
        for i in range(population_size):
            solution = parent_solver.create_initital_solution("random")
            solutions.append(solution)
        return solutions