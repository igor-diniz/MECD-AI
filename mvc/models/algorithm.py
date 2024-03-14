from helpers.file_reader import FileReader
from metaheuristics.hill_climbing import HillClimbingSolver
from metaheuristics.simulated_annealing import SimulatedAnnealing
from metaheuristics.tabu_search import TabuSearchSolver
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from copy import deepcopy
      
class HCModel:
    def solve(self, file, id, solve_params):
        total_books, libraries, total_days = FileReader().read(file)
        hc = HillClimbingSolver(total_books,
                                deepcopy(libraries),
                                total_days)
        initial_solution = hc.create_initial_solution(mode=solve_params[0])
        hc.solve(initial_solution=initial_solution,
             num_iterations=solve_params[1],
             results_csv='analysis/hc/',
             solution_id=id,
             filename=file,
             timeout=3600
            )
        
    
