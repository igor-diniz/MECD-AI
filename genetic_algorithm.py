from helpers.file_reader import FileReader
from helpers.solution import Solution
from metaheuristics.solver import Solver

file_reader = FileReader()
total_books, libraries, total_days = file_reader.read("data/a_example.in")
    
parent_solver =  Solver(total_books, libraries, total_days)
random_initital_solution = parent_solver.create_initital_solution("random")
greedy_initital_solution = parent_solver.create_initital_solution("greedy")

def generate_population(population_size):
    solutions = []
    for i in range(population_size):
        solutions.append(random_initital_solution("random"))
    return solutions

def cross_over(actual_solution: Solution):
    libraries_solution = random_initital_solution.libraries
    [print(str(library)) for library in libraries_solution]

def generic_algorithm(actual_solution: Solution):
    solutions = generate_population(solutions)

    libraries_solution = random_initital_solution.libraries
    [print(str(library)) for library in libraries_solution]

    books = random_initital_solution.books
    [print(str(book)) for book in books]

