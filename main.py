from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm

def solve(file_name, population_size, n_generations, mutate_mode, crossover_mode):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    ga = GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(
        population_size=population_size,
        n_generations=n_generations,
        mutate_mode=mutate_mode,
        crossover_mode=crossover_mode,
        results_csv="analysis/ga/ga_results.csv",
        filename=file_name
    )

if __name__ == "__main__":
    # Define the grid of parameters to search
    population_size = 25
    n_generations = 10
    mutate_modes = ["swap", "addition", "deletion"]
    crossover_modes = ["mid", "random"]

    # Perform grid search
    for mutate_mode in mutate_modes:
        for crossover_mode in crossover_modes:
            solve("data/f_libraries_of_the_world.in", population_size, n_generations, mutate_mode, crossover_mode)