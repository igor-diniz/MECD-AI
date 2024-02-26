from helpers.file_reader import FileReader
from metaheuristics.genetic_algorithm import GeneticAlgorithm

def solve(file_name):
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(file_name)
    
    ga =  GeneticAlgorithm(total_books, libraries, total_days)
    ga.solve(
        population_size=25,
        n_generations=5,
        mutate_mode="random",
        crossover_mode="mid"
    )

if __name__ == "__main__":
    solve("data/a_example_2.in")