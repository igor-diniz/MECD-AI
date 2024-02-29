import time
import tracemalloc
from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from metaheuristics.hill_climbing import HillClimbingSolver
from metaheuristics.simulated_annealing import SimulatedAnnealing
from metaheuristics.tabu_search import TabuSearchSolver
from metaheuristics.solver import Solver
from helpers import utils
import uuid


def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)

    parent_solver = Solver(total_books, libraries, total_days)
    initial_sol_mode = "random"

    start_time = time.time()
    tracemalloc.start()
    tracemalloc.clear_traces()
    
    initial_solution = parent_solver.create_initial_solution(initial_sol_mode)

    end_time = time.time()
    elapsed_time = end_time - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    uuid4 = str(uuid.uuid4())

    hc = HillClimbingSolver(total_books, libraries, total_days)
    hc.solve(
            initial_solution,
            num_iterations=100,
            log = True,
            results_csv="analysis/hc",
            solution_id=uuid4,
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
            solution_id=uuid4,
            filename=file_name
            )
    
    ts = TabuSearchSolver(total_books, libraries, total_days)
    ts.solve(
              initial_solution,
              tabu_tenure=9,
              n_neighbours=-1,
              max_iterations=100,
              log=True,
              results_csv="analysis/ts",
              solution_id=uuid4,
              filename=file_name
              )
    
    ga = GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(
        population_size=300,
        n_generations=15,
        mutate_mode="swap",
        crossover_mode="mid",
        results_csv="analysis/ga",
        solution_id=uuid4,
        filename=file_name
    )

    merged_df = utils.merge_metrics_dataframes("analysis")
    print(merged_df)
    
    utils.compare_algorithms(data_df=merged_df,
                             id=uuid4,
                             algorithms=["HC", "SA", "TS", "GA"], 
                             initial_score=initial_solution.evaluate(), 
                             initial_time=elapsed_time, 
                             initial_memory=peak_memory,
                             save=False,
                             analysis_folder="analysis")


if __name__ == "__main__":
    solve("data/a_example_2.in")
