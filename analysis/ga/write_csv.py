"""Only run this once before solving the problem!"""
import pandas as pd

ga_results = pd.DataFrame(columns=["filename", "population_size", "n_generations", "mutate_mode", "crossover_mode", "best_score", "fittest", "time"])
ga_results.to_csv("analysis/ga/ga_results.csv", index=None)