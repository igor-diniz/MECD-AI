from metaheuristics.solver import Solver
from helpers.solution import Solution
from helpers.utils import results_to_csv
from copy import deepcopy
import numpy as np
import math
import random
import time
import csv

class GeneticAlgorithm(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days
    
    def solve(self, population_size, n_generations, mutate_mode, crossover_mode, log=False, results_csv=None, filename=None):
        start_time = time.time()
        print("Generating population...")

        # Generate first population (generation 0)
        population = self.generate_population(population_size)
        print(f"Population with {population_size} individuals generated!")
        fittest = population.individuals[0]
        best_score = fittest.evaluate()
        fittest_generation = 0

        num_iterations = n_generations
        generation = 0

        while(num_iterations > 0):
            generation += 1
            print(f"-----\nWorking on generation {generation}...")
            tournment_winner_sol = population.tournament_select(4)
            roulette_winner_sol = population.roulette_select()
            
            # Next generation
            child_1, child_2 = population.cross_over(tournment_winner_sol,
                                                                     roulette_winner_sol,
                                                                     crossover_mode)
            # Mutate children: 10% chance to perform mutation
            if np.random.randint(0, 10) < 1:
                child_1 = population.mutate(child_1, mutate_mode)
                child_2 = population.mutate(child_2, mutate_mode)

            # Replace least fittest with child
            population.replace_least_fittest(child_1)
            population.replace_least_fittest(child_2)
            
            # Checking the greatest fit among the current population
            greatest_fit = population.get_greatest_fit()
            if fittest.__lt__(greatest_fit):
                fittest = greatest_fit
                best_score = greatest_fit.evaluate()
                fittest_generation = generation
                if log:
                    print(f"\nGeneration: {generation }")
                    print(f"Solution: {fittest}, score: {best_score}")
                    print(population)
            num_iterations -= 1
            print(f"End of generation {generation}!")

            
        print(f"-----\n  Final solution: {fittest}, score: {best_score}")
        print(f"  Found on generation {fittest_generation}")
        
        end_time = time.time()
        print(f"-----\nElapsed time: {end_time - start_time} seconds")

        # Write results to csv, if csv file is provided
        if results_csv and filename:
            results_to_csv(results_csv, filename, population_size, n_generations,
                                mutate_mode, crossover_mode, best_score, fittest.__str__(), end_time)
            print(f"Result written to {results_csv}.")
        
        return fittest
    
    def generate_population(self, population_size: int):
        # Generate population with random individuals
        population = []
        copy_solver = deepcopy(self)
        for i in range(population_size):
            copy_solver.clear()
            copy_solver = GeneticAlgorithm(self.total_books,
                                           self.libraries,
                                           self.total_days)
            individual = copy_solver.create_initial_solution("random")
            population.append(individual)
        return Population(len(population),
                          population,
                          self.total_books,
                          self.libraries,
                          self.total_days)

class Population(GeneticAlgorithm):
    def __init__(self, size: int, individuals: list, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days
        self.size = size
        self.individuals = individuals
    
    def tournament_select(self, tournament_size: int):
        # Select best individual among tournament competitors
        individuals = deepcopy(self.individuals)
        best_solution = individuals[0]
        for i in range(tournament_size):
            index = np.random.randint(0, len(individuals))
            if best_solution.__le__(individuals[index]):
                best_solution = individuals[index]
            del individuals[index]
        return best_solution
    
    def roulette_select(self):
        # Select individual based on score probability
        individuals = deepcopy(self.individuals)
        score_sum = sum([solution.evaluate() for solution in self.individuals])
        selection_probabilities = [solution.evaluate() / score_sum for solution in individuals]
        return individuals[np.random.choice(len(individuals), p=selection_probabilities)]

    def cross_over(self, individual_1: Solution, individual_2: Solution, mode: str):
        if mode.lower() == "mid":
            # Mid point cross-over
            index_1 = math.trunc(len(individual_1.libraries) / 2)
            index_2 = math.trunc(len(individual_2.libraries) / 2)
            child_1_libraries = np.append(individual_1.libraries[0:index_1], individual_2.libraries[index_2:]).tolist()
            child_2_libraries = np.append(individual_2.libraries[0:index_1], individual_1.libraries[index_2:]).tolist()    
        else:
            # Random point cross-over
            index_1 = random.randint(1, len(individual_1.libraries) - 1)
            index_2 = random.randint(1, len(individual_2.libraries) - 1)
            child_1_libraries = np.append(individual_1.libraries[0:index_1], individual_2.libraries[index_2:]).tolist()
            child_2_libraries = np.append(individual_1.libraries[index_1:], individual_2.libraries[0:index_2]).tolist()

         # Remove repeated libraries from each child, then select books
        child_1 = self.select_library_books(list(dict.fromkeys(child_1_libraries)))
        child_2 = self.select_library_books(list(dict.fromkeys(child_2_libraries)))

        return child_1, child_2
    
    def mutate(self, individual: Solution, mode: str):
        if mode.lower() == "random":
            mode = random.choice(["swap", "deletion", "addition"])
        if mode.lower() == "swap":
            return self.get_internal_neighbour(individual, "swap")
        if mode.lower() == "deletion":
            return self.get_internal_neighbour(individual, "deletion")
        if mode.lower() == "addition":
            return self.get_external_neighbour(individual)
        

    def replace_least_fittest(population, offspring):
        # Start with first index
        least_fittest_index = 0

        # Get least fit individual in population
        for i in range(1, len(population.individuals)):
            if population.individuals[i].__le__(population.individuals[least_fittest_index]):
                least_fittest_index = i

        # Replace least fit individual with offspring
        population.individuals[least_fittest_index] = offspring

    def get_greatest_fit(self):
        # Get fittest individual in population
        best_solution = self.individuals[0]
        best_score = best_solution.evaluate()
        for i in range(1, len(self.individuals)):
            score = self.individuals[i].evaluate()
            if score > best_score:
                best_score = score
                best_solution = self.individuals[i]
        return best_solution

    def __str__(self):
        population = (f"size: {self.size}\nindividuals:")
        for i in range(len(self.individuals)):
            population += f"\n\tSolution {i+1}:"
            population += f"\t\t{self.individuals[i]}\n"
        return population