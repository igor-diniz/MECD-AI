from metaheuristics.solver import Solver
from helpers.solution import Solution
from helpers.utils import results_to_csv, plot_evolution_log
from copy import deepcopy
import numpy as np
import math
import random
import time
import tracemalloc

class GeneticAlgorithm(Solver):
    def __init__(self, total_books, libraries, total_days):
        super().__init__(total_books, libraries, total_days)
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days
        self.curr_sol_history = []
    
    def solve(self, population_size: int,
              n_generations: int,
              mutate_mode: str,
              crossover_mode: str,
              log=False,
              evolution_log: bool = False,
              results_csv=None,
              solution_id: str=None,
              filename=None,
              timeout: int=3600):
        
        start_time = time.time()
        tracemalloc.start()
        tracemalloc.clear_traces()

        # Clear current solution history for each call of solve
        self.curr_sol_history.clear()

        print("Generating population...")

        # Generate first population (generation 0)
        population = self.generate_population(population_size)
        print(f"Population with {population_size} individuals generated!")
        fittest = population.individuals[0]
        best_score = fittest.evaluate()
        fittest_generation = 0

        num_iterations = n_generations
        generation = 0

        if evolution_log:
            generations_log = []
            generations_log.append([individual.evaluate() for individual in population.individuals])

        while num_iterations > 0 and time.time() - start_time < timeout:
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
            self.curr_sol_history.append(greatest_fit.evaluate())
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
            
            if evolution_log:
                generations_log.append([individual.evaluate() for individual in population.individuals])
            
        print(f"-----\n  Final solution: {fittest}, score: {best_score}")
        print(f"  Found on generation {fittest_generation}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"-----\nElapsed time: {elapsed_time} seconds\nPeak memory: {peak_memory} bytes")

        # Write results to csv, if csv file is provided
        if results_csv and filename:
            results_to_csv(results_csv, self.curr_sol_history, solution_id, filename, population_size, (n_generations, fittest_generation),
                                mutate_mode, crossover_mode, best_score, elapsed_time, peak_memory)
        
        if evolution_log:
            plot_evolution_log(filename, generations_log, save=True, id=solution_id)
        
        return fittest
    
    def generate_population(self, population_size: int):
        """Generates initial population, composed by 50% random individuals and
        50% greedy-originated individuals."""

        population = Population(total_books=self.total_books,
                          libraries=self.libraries,
                          total_days=self.total_days)
    
        copy_solver = deepcopy(self)
        
        # Greedy-originated individual
        n_greedy = round(population_size*0.5)

        copy_solver = GeneticAlgorithm(self.total_books,
                                           deepcopy(self.libraries),
                                           self.total_days)
        greedy_individual = copy_solver.create_initial_solution("greedy")
        population.individuals.append(greedy_individual)

        for i in range(n_greedy-1):
            individual = population.mutate(deepcopy(greedy_individual), "random")
            population.individuals.append(individual)

        # Random individuals
        for i in range(population_size-n_greedy):
            copy_solver.clear()
            copy_solver = GeneticAlgorithm(self.total_books,
                                           deepcopy(self.libraries),
                                           self.total_days)
            individual = copy_solver.create_initial_solution("random")
            population.individuals.append(individual)

        population.size = len(population.individuals)

        return population

class Population(GeneticAlgorithm):
    def __init__(self, size: int=None, individuals: list=[], total_books=None, libraries=None, total_days=None):
        super().__init__(total_books, libraries, total_days)
        self.total_books = total_books
        self.libraries = libraries
        self.total_days = total_days
        self.size = size
        self.individuals = individuals
    
    def tournament_select(self, tournament_size: int):
        """Performs tournament selection. A number of individuals (tournament_size)
        is selected from the population, and the fittest individual among the chosen
        wins the tournament"""

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
        """Performs roulette wheel selection, which selects an individual based on
        score probability. If an individual has higher score, it is more likely to
        be chosen in the roulette"""

        individuals = deepcopy(self.individuals)
        score_sum = sum([solution.evaluate() for solution in self.individuals])
        selection_probabilities = [solution.evaluate() / score_sum for solution in individuals]
        return individuals[np.random.choice(len(individuals), p=selection_probabilities)]

    def cross_over(self, individual_1: Solution, individual_2: Solution, mode: str):
        """Performs cross-over from two parent individuals. The cross-over modes can be
        mid- or random point. The mode defines the position on which the crossover will
        occur"""

        if mode.lower() == "mid":
            # Mid point cross-over
            index_1 = math.trunc(len(individual_1.libraries) / 2)
            index_2 = math.trunc(len(individual_2.libraries) / 2)
            child_1_libraries = np.append(individual_1.libraries[0:index_1], individual_2.libraries[index_2:]).tolist()
            child_2_libraries = np.append(individual_2.libraries[0:index_1], individual_1.libraries[index_2:]).tolist()    
        else:
            # Random point cross-over
            index_1 = random.randint(1, len(individual_1.libraries))
            index_2 = random.randint(1, len(individual_2.libraries))
            child_1_libraries = np.append(individual_1.libraries[0:index_1], individual_2.libraries[index_2:]).tolist()
            child_2_libraries = np.append(individual_1.libraries[index_1:], individual_2.libraries[0:index_2]).tolist()

         # Remove repeated libraries from each child, then select books
        child_1 = self.select_library_books(list(dict.fromkeys(child_1_libraries)))
        child_2 = self.select_library_books(list(dict.fromkeys(child_2_libraries)))

        return child_1, child_2
    
    def mutate(self, individual: Solution, mode: str):
        """Mutates the individual using get_internal_neighbour or 
        get_external_neighour methods"""

        if mode.lower() == "random":
            mode = random.choice(["internal swap", "deletion", "external swap"])
        if mode.lower() == "internal swap":
            return self.get_internal_neighbour(individual, "swap")
        if mode.lower() == "deletion":
            return self.get_internal_neighbour(individual, "deletion")
        if mode.lower() == "external swap":
            return self.get_external_neighbour(individual)
        

    def replace_least_fittest(population, offspring):
        """Replace the least fit individual from population with the offsprings"""
        # Start with first index
        least_fittest_index = 0

        # Get least fit individual in population
        for i in range(1, len(population.individuals)):
            if population.individuals[i].__le__(population.individuals[least_fittest_index]):
                least_fittest_index = i

        # Replace least fit individual with offspring
        population.individuals[least_fittest_index] = offspring

    def get_greatest_fit(self):
        """Get fittest individual from population"""
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