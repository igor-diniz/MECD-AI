import csv
from operator import itemgetter
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def results_to_csv(csv_path: str, curr_solution_history: list,
                    *columns):
        
        data = columns
        metrics_filename = csv_path + "/metrics.csv"

        with open(metrics_filename, mode='a+', newline='') as file:
            writer = csv.writer(file)

            file.seek(0)
            rows = file.readlines()

            if len(rows) > 1:  # Check if there is more than just the header row
                last_row = rows[-1]
                next_row_id = int(last_row[0]) + 1
            else: 
                next_row_id = 1

            writer.writerow([next_row_id, *data])

        save_history(csv_path, next_row_id, curr_solution_history)


def save_history(csv_path: str, id: int, curr_solution_history: list):
        history_filename = csv_path + "/solutions_history.csv"

        with open(history_filename, mode='a+', newline='') as file:
            writer = csv.writer(file)

            # Write the solution history to the CSV file
            for solution_score in curr_solution_history:
                writer.writerow([id, solution_score])   


def grid_search_ga(function, parameters: dict, filename):
    population_size, n_generations, mutate_modes, crossover_modes = itemgetter("population_size",
                                                                               "n_generations",
                                                                               "mutate_modes", 
                                                                               "crossover_modes")(parameters)

    # Perform grid search
    for mutate_mode in mutate_modes:
        for crossover_mode in crossover_modes:
            function(filename, population_size, n_generations, mutate_mode, crossover_mode)


def merge_metrics_dataframes(analysis_folder):
    # Initialize an empty DataFrame to store merged metrics
    merged_metrics_df = pd.DataFrame(columns=["ID", "File Instance"])

    # Iterate through files in the analysis folder
    for root, dirs, files in os.walk(analysis_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith("metrics.csv"):
                metrics_df = pd.read_csv(file_path)
                merged_metrics_df = pd.merge(merged_metrics_df, metrics_df, on=["ID", "File Instance"], how="outer", suffixes=('_merged', '_metrics'))

    return merged_metrics_df


def compare_algorithms(data_df, id):
    algorithms = ['GA', 'SA', 'Tabu', 'HC', 'Initial']
    metrics = ['Score', 'Time', 'Memory']

    sns.set_style("whitegrid")
    fig, axes = plt.subplots(len(metrics), 1, figsize=(5, 10))

    id_data = data_df[data_df['ID'] == id]

    for i, metric in enumerate(metrics):
        data = pd.DataFrame()
        for algorithm in algorithms:
            data[algorithm] = id_data[f"{algorithm} {metric}"]
        
        sns.barplot(data=data, ax=axes[i])
        axes[i].set_xlabel('Algorithm')
        axes[i].set_ylabel(metric)
        axes[i].set_title(f"Comparison of {metric} for Different Algorithms (ID={id})")

        # Set the value of each bar
        for bar in axes[i].patches:
            axes[i].annotate(format(bar.get_height(), '.2f'), 
                             (bar.get_x() + bar.get_width() / 2, 
                              bar.get_height()), 
                             ha='center', va='center', 
                             size=10, xytext=(0, 2.5),
                             textcoords='offset points')

    plt.tight_layout()
    plt.show()