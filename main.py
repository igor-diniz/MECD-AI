from helpers.file_reader import FileReader
from metaheuristics.solver import Solver

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    parent_solver =  Solver(total_books, libraries, total_days)

    print("Random Initial Solution")
    random_initial_solution = parent_solver.create_initial_solution("random")
    print(random_initial_solution)
    parent_solver.clear()
    new_neighbor = parent_solver.get_internal_neighbour(random_initial_solution)
    print("Neighbor Solution")
    print(new_neighbor)
    
    #print()
    
#
    #print("Greedy Initial Solution")
    #greedy_initial_solution = parent_solver.create_initial_solution("greedy")
    #print(greedy_initial_solution)

if __name__ == "__main__":
    solve("data/a_example.in")