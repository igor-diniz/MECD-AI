from helpers.file_reader import FileReader
from metaheuristics.solver import Solver

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    print("Random Initial Solution")
    parent_solver =  Solver(total_books, libraries, total_days)
    random_initital_solution = parent_solver.create_initital_solution("random")
    print(random_initital_solution)
    print()

    #print("Greedy Initial Solution")
    #parent_solver_greedy =  Solver(total_books, libraries, total_days)
    #greedy_initital_solution = parent_solver_greedy.create_initital_solution("greedy")
    #print(greedy_initital_solution)

if __name__ == "__main__":
    solve("data/a_example.in")