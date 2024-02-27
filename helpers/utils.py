import csv
from operator import itemgetter

def results_to_csv(csv_path: str,
                    *columns):
        
        data = columns

        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)


def grid_search_ga(function, parameters: dict, filename):
    population_size, n_generations, mutate_modes, crossover_modes = itemgetter("population_size",
                                                                               "n_generations",
                                                                               "mutate_modes", 
                                                                               "crossover_modes")(parameters)

    # Perform grid search
    for mutate_mode in mutate_modes:
        for crossover_mode in crossover_modes:
            function(filename, population_size, n_generations, mutate_mode, crossover_mode)