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
        save_log=True,
        results_csv="analysis/ga/results.csv",
        filename=file_name
    )

if __name__ == "__main__":
    files = [#"data/a_example_2.in",
             "data/b_read_on.in",
             "data/c_incunabula.in",
             "data/d_tough_choices.in",
             "data/e_so_many_books.in",
             "data/f_libraries_of_the_world.in"
             ]
    params = {"population_size": 20,
              "n_generations": 10,
              "mutate_modes": ["deletion", "swap", "addition"],
              "crossover_modes": ["mid", "random"]}

    for filename in files:
        grid_search_ga(solve,
                params,
                 filename)