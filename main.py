from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from metaheuristics.hill_climbing import HillClimbingSolver
from metaheuristics.simulated_annealing import SimulatedAnnealing
from metaheuristics.solver import Solver

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)

    parent_solver = Solver(total_books, libraries, total_days)
    initial_solution = parent_solver.create_initial_solution("random")

    hc = HillClimbingSolver(total_books, libraries, total_days)
    hc.solve(
            initial_solution,
            num_iterations=100,
            log = True,
            results_csv="analysis/hc",
            filename=file_name
        )
    
    sa = SimulatedAnnealing(total_books, libraries, total_days)
    sa.solve(
            initial_solution,
            num_iterations=100,
            T=1000, 
            cooling_schedule=0.99,
            log=True,
            results_csv="analysis/sa",
            filename=file_name
            )
    
    ga = GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(
        population_size=300,
        n_generations=15,
        mutate_mode="swap",
        crossover_mode="mid",
        results_csv="analysis/ga",
        filename=file_name
    )


if __name__ == "__main__":
    solve("data/a_example_2.in")
