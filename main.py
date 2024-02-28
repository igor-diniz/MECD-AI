from helpers.file_reader import FileReader
from metaheuristics.solver import Solver
from metaheuristics.tabu_search import TabuSearchSolver
import time
import tracemalloc

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    tabu_solver =  TabuSearchSolver(total_books, libraries, total_days)

    print("Initial Solution")
    mode = "greedy"

    start_time = time.time()
    tracemalloc.start()
    tracemalloc.clear_traces()

    initial_solution = tabu_solver.create_initial_solution(mode)

    initial_time = time.time() - start_time
    _, initial_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(initial_solution)
    
    print()

    print("Tabu Search Solution")
    tabu_tenure=7
    n_neighbours=15
    max_iterations=100
    start_time = time.time()
    tracemalloc.start()
    tracemalloc.clear_traces()

    best_solution = tabu_solver.solve(initial_solution, tabu_tenure=tabu_tenure, n_neighbours=n_neighbours, max_iterations=max_iterations, log=True)

    tabu_time = time.time() - start_time
    _, tabu_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(best_solution)


    tabu_solver.save_metrics(file_name, initial_solution.evaluate(), 
                                    initial_time, initial_memory, mode, best_solution.evaluate(), 
                                    tabu_time, tabu_memory, tabu_tenure, n_neighbours, max_iterations)

if __name__ == "__main__":
    solve("data/a_example_4.in")