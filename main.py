from helpers.file_reader import FileReader
from metaheuristics.solver import Solver
from metaheuristics.hill_climbing import HillClimbingSolver
from metaheuristics.simulated_annealing import SimulatedAnnealing

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    simulated_annealing_solver = SimulatedAnnealing(total_books, libraries, total_days)

    print("Random Initial Solution")
    random_initial_solution = simulated_annealing_solver.create_initial_solution("random")
    print(random_initial_solution)

    neighbor = simulated_annealing_solver.get_internal_neighbour
    neighbor2 = simulated_annealing_solver.get_external_neighbour
    
    print()

    print("Simulated Annealing Solution")
    best_solution = simulated_annealing_solver.solve(random_initial_solution, neighbor,neighbor2, 1000)
    print(best_solution)

    #neighbor_selected= simulated_annealing_solver.select_neighbor_generator(random_initial_solution,neighbor,neighbor2)
    #print(neighbor_selected)


    #return best_solution

if __name__ == "__main__":
    solve("data/a_example_2.in")
