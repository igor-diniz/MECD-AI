from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
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
