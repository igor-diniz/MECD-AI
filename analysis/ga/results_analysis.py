import pandas as pd

ga_results = pd.read_csv("analysis/ga/ga_results.csv")

ga_results_b = ga_results[ga_results["filename"] == "data/b_read_on.in"]
ga_results_c = ga_results[ga_results["filename"] == "data/c_incunabula.in"]
ga_results_d = ga_results[ga_results["filename"] == "data/d_tough_choices.in"]
ga_results_e = ga_results[ga_results["filename"] == "data/e_so_many_books.in"]
ga_results_f = ga_results[ga_results["filename"] == "data/f_libraries_of_the_world.in"]

print(ga_results.iloc[ga_results_f['best_score'].idxmax()])