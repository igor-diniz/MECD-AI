from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from helpers.utils import grid_search_ga

def solve(file_name, population_size, n_generations, mutate_mode, crossover_mode):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    ga = GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(
        population_size=population_size,
        n_generations=n_generations,
        mutate_mode=mutate_mode,
        crossover_mode=crossover_mode,
        save_log=True
    )

if __name__ == "__main__":
   
    filename = "data/a_example.in"
    params = {"population_size": 5,
              "n_generations": 3,
              "mutate_modes": ["deletion", "swap", "addition"],
              "crossover_modes": ["mid", "random"]}
    grid_search_ga(solve,
                   params,
                   filename)