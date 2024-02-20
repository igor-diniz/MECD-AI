from helpers.solution import Solution
import random

class Solver:
    def __init__(self, total_books, libraries, total_days):
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days 

    def create_random_solution(self):
        # WIP
        sign_up_total = 0
        libraries = []
        books = []
        while sign_up_total < self.total_days:
            library = random.choice(list(self.libraries.keys()))
            libraries.append(library)

            book = max(list(self.library.book_list()), key= lambda book: book.score)
            books.append(book)

   
    def evaluate_solution(self, solution: Solution):
        books = solution.books
        total_score = 0
        for book in books:
            total_score += book.score

        return total_score
    
    def is_solution_feasible(self, solution: Solution):
        libraries = solution.libraries
        return libraries[0].signup_days < self.total_days
    
    def solve(self):
        # WIP
        return None


