import threading
from ui.configs.constants import HC, SA, TS, GA
from metaheuristics.solver import Solver
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from metaheuristics.tabu_search import TabuSearchSolver
from metaheuristics.hill_climbing import HillClimbingSolver
from metaheuristics.simulated_annealing import SimulatedAnnealing
from copy import deepcopy

def run_thread(function):
    threading.Thread(target=function).start()

def go_to_page(master, page):
    clear_content(master)
    page(master=master)

def clear_content(master):
    for widget in master.winfo_children():
        widget.destroy()

def go_to_algorithm_page(master, page, algorithm, file, solve_params):
    clear_content(master)
    page(master,algorithm,file, solve_params)

def go_to_compare_results_page(master, page, file, check_alg, solve_params):
    clear_content(master)
    page(master, file, check_alg, solve_params)

def compare_algorithms(file, id, total_books, libraries, total_days,
                       check_alg,
                       hc_solve_params,
                       sa_solve_params, ts_solve_params,
                       ga_solve_params):
    
    libraries = deepcopy(libraries)
    
    if check_alg[0] == 1:
        solve_hc(file, id, total_books, libraries, total_days, hc_solve_params)
    if check_alg[1] == 1:
        solve_sa(file, id, total_books, libraries, total_days, sa_solve_params)
    if check_alg[3] == 1:
        solve_ts(file, id, total_books, libraries, total_days, ts_solve_params)
    if check_alg[4] == 1:
        solve_ga(file, id, total_books, libraries, total_days, ga_solve_params)

def solve_hc(file, id, total_books, libraries, total_days, solve_params):
    hc = HillClimbingSolver(total_books, libraries, total_days)
    initial_solution = hc.create_initial_solution(mode=solve_params[0])
    hc.solve(initial_solution=initial_solution,
             num_iterations=solve_params[1],
             results_csv='analysis/hc/',
             solution_id=id,
             filename=file,
             timeout=3600
            )
    
def solve_sa(file, id, total_books, libraries, total_days, solve_params):
    sa = SimulatedAnnealing(total_books, libraries, total_days)
    initial_solution = sa.create_initial_solution(mode=solve_params[0])
    sa.solve(initial_solution=initial_solution,
             num_iterations=solve_params[1],
             T = solve_params[2],
             cooling_schedule=solve_params[3],
             results_csv='analysis/sa/',
             solution_id=id,
             filename=file,
             timeout=3600)
    
def solve_ts(file, id, total_books, libraries, total_days, solve_params):
    ts = TabuSearchSolver(total_books, libraries, total_days)
    initial_solution = ts.create_initial_solution(mode=solve_params[0])
    ts.solve(initial_solution=initial_solution,
             tabu_tenure=solve_params[1],
             n_neighbours=solve_params[2],
             max_iterations=solve_params[3],
             results_csv='analysis/ts/',
             solution_id=id,
             filename=file,
             timeout=3600
            )
    
def solve_ga(file, id, total_books, libraries, total_days, solve_params):
    ga = GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(population_size=solve_params[0],
             n_generations=solve_params[1],
             mutate_mode=solve_params[2],
             crossover_mode=solve_params[3],
             results_csv="analysis/ga",
             solution_id=id,
             filename=file,
             timeout=3600
            )