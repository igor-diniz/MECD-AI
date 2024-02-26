from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    ga =  GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(
        population_size=50,
        n_generations=10,
        mutate_mode="random",
        crossover_mode="mid",
        results_csv="analysis/ga/ga_results.csv",
        filename=file_name
    )

if __name__ == "__main__":
    solve("data/b_read_on.in")