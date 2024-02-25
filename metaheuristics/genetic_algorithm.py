from metaheuristics.solver import Solver
from copy import deepcopy
import numpy as np

class GeneticAlgorithm(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days
    
    def generate_population(self, population_size: int):
        solver =  GeneticAlgorithm(self.total_books, self.libraries, self.total_days)
        population = []
        for i in range(population_size):
            solver.clear()
            solver =  GeneticAlgorithm(self.total_books, self.libraries, self.total_days)
            solution = solver.create_initial_solution("random")
            population.append(solution)
        return Population(size = len(population) + 1, individuals= population)

    def mutate(self, individual):
        return self.get_internal_neighbour(individual, "swap")
    
class Population(GeneticAlgorithm):
    def __init__(self, size: int, individuals: list):
        self.size = size
        self.individuals = individuals
    
    def tournament_select(self, tournament_size: int):
        individuals = deepcopy(self.individuals)
        best_solution = individuals[0]
        for i in range(tournament_size-1):
            solver =  GeneticAlgorithm(self.total_books, self.libraries, self.total_days)
            index = np.random.randint(0, len(individuals))
            print(individuals[index]) 
            if best_solution.__le__(individuals[index]):
                best_solution = individuals[index]
            del individuals[index]
            solver.clear()
        return best_solution

    def __str__(self):
        population = f"size: {self.size}\nindividuals:"
        for i in range(len(self.individuals)):
            population += f"\n\tSolution {i+1}:"
            population += f"\t\t{self.individuals[i]}\n"
        return population