from helpers.file_reader import FileReader
from metaheuristics.solver import Solver
from metaheuristics.tabu_search import TabuSearchSolver

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    tabu_solver =  TabuSearchSolver(total_books, libraries, total_days, tabu_tenure=10, max_iterations=1000)

    print("Random Initial Solution")
    random_initial_solution = tabu_solver.create_initial_solution("random")
    print(random_initial_solution)
    
    print()

    print("Tabu Search Solution")
    best_solution = tabu_solver.solve(random_initial_solution)
    print(best_solution)


if __name__ == "__main__":
    solve("data/a_example_2.in")