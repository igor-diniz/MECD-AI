from helpers.solution import Solution
import random

class Solver:
    def __init__(self, total_books, libraries, total_days):
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days 

    def create_random_solution(self):
        sign_up_total = 0
        libraries = []
        books = []
        while sign_up_total < self.total_days:
            library = random.choice(list(self.libraries.keys()))
            libraries.append(library)

            book = max(list(self.libraries.book_list()), key= lambda book: book.score)
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
    
    def solve(self, ):




"""
Solutions:
[L1, L2, L3], [book1.L1, book2.L1, book3.L2, book6.L3, book7.L3]
[L4, L2, L3], [book9.L4, book10.L4, book11.L4, book3.L2, book7.L3]

"""


