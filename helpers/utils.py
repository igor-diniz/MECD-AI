import csv
from operator import itemgetter
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def results_to_csv(csv_path: str, curr_solution_history: list,
                    *columns):
        
        data = [*columns]
        metrics_filename = csv_path + "/metrics.csv"

        with open(metrics_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

        save_history(csv_path, data[0], curr_solution_history)


def save_history(csv_path: str, id: int, curr_solution_history: list):
        history_filename = csv_path + "/solutions_history.csv"

        with open(history_filename, mode='a', newline='') as file:
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

def plot_evolution_log(filename: str, evolution_log, save: bool=False, id=None):
    # Plot 10 generations
    evolution_log = np.array(evolution_log)
    stride = len(evolution_log) // 10
    print(stride)
    indices = np.round(np.linspace(0, len(evolution_log) - 1, 10)).astype(int)

    title = f"Population evoluion: {filename}"
    fig_rows = 2
    fig_cols = 5
    print(indices)
    subplots_indexes = []
    for i in range(fig_rows):
        for j in range(fig_cols):    
            subplots_indexes.append((i, j))

    fig, axs = plt.subplots(nrows=fig_rows, ncols=fig_cols, sharex=True, sharey=True, figsize=(12, 7))

    for generation, (i, j) in zip(indices, subplots_indexes):
        x = [individual for individual in range(1, len(evolution_log[generation])+1)]
        y = evolution_log[generation]
        axs[i, j].plot(x, y, '-ok', markersize=3)
        axs[i, j].set_title(f"Gen {generation}")

    fig.text(0.5, 0.04, 'Individuals', ha='center')
    fig.text(0.04, 0.5, 'Scores', va='center', rotation='vertical')
    fig.text(0.5, 0.95, title, ha='center', size=14)

    plt.subplots_adjust(left=0.08,
                    bottom=0.1,  
                        top=0.89,
                        wspace=0.1,
                        hspace=0.2)
    if save:
         plt.savefig(f'analysis/ga/evolution_log/{filename}_{id}.png')

def merge_metrics_dataframes(analysis_folder):
    # Initialize an empty DataFrame to store merged metrics
    merged_metrics_df = pd.DataFrame(columns=["ID", "File Instance"])

    # Iterate through files in the analysis folder
    for root, dirs, files in os.walk(analysis_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith("metrics.csv"):
                metrics_df = pd.read_csv(file_path)
                merged_metrics_df = pd.merge(merged_metrics_df, metrics_df, on=["ID", "File Instance"], how="outer")

    return merged_metrics_df


def compare_algorithms(data_df: pd.DataFrame, 
                       id: int, 
                       algorithms: list, 
                       initial_score, 
                       initial_time: float, 
                       initial_memory: float, 
                       save: bool=True, 
                       analysis_folder: str="analysis"):
    
    metrics = ['Score', 'Time', 'Memory']
    initial_metrics = [initial_score, initial_time, initial_memory]
    colors = ["#051821", "#1A4645", "#266867", "#F58800", "#F8BC24"]

    sns.set_style("whitegrid")
    fig, axes = plt.subplots(len(metrics), 1, figsize=(8, 8))
    fig.suptitle(f"Comparison for Different Algorithms\n\n")

    id_data = data_df[data_df['ID'] == id]

    for i, metric in enumerate(metrics):
        data = pd.DataFrame()
        for algorithm in algorithms:
            data[algorithm] = id_data[f"{algorithm} {metric}"]
        
        data[f"Initial"] = initial_metrics[i]
        
        sns.barplot(data=data, ax=axes[i], palette=colors[:len(algorithms) + 1])

        axes[i].set_ylabel(metric)
        
        if i == len(metrics) - 1:
            axes[i].set_xlabel('Algorithm')

        # Set the value of each bar
        for bar in axes[i].patches:
            axes[i].annotate(format(bar.get_height(), '.2f'), 
                             (bar.get_x() + bar.get_width() / 2, 
                              bar.get_height()), 
                             ha='center', va='center', 
                             size=10, xytext=(0, 3.5),
                             textcoords='offset points')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)

    if save:
         plt.savefig(f'{analysis_folder}/images/{id}_comparison.png')

    plt.show()


def plot_solution_history(id: str, algorithm: str, save: bool=True, analysis_folder: str="analysis"):
    solutions_history_df = pd.read_csv(f"{analysis_folder}/{algorithm}/solutions_history.csv")
    metrics_df = pd.read_csv(f"{analysis_folder}/{algorithm}/metrics.csv")
    merged_df = pd.merge(solutions_history_df, metrics_df, on="ID")

    id_df = merged_df[merged_df["ID"] == id]

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(id_df)), id_df['Solution History'], color="black", label="Solution History")

    handles = []
    labels = []
    for column in id_df.columns:
        if column not in ['ID', 'File Instance', 
                          f'{algorithm.upper()} Score', 
                          f'{algorithm.upper()} Time', 
                          f'{algorithm.upper()} Memory', 
                          'Solution History']:
            
            label = f"{column}: {id_df[column].iloc[0]}"
            handle, = plt.plot([], [], 'o', color='white', label=label)
            handles.append(handle)
            labels.append(label)
    plt.xlabel('Iterations')
    plt.ylabel('Current Solution Score')
    plt.title(f"{id_df['File Instance'].iloc[0]} solution history for {algorithm}")
    plt.legend(handles, labels, loc='upper right', bbox_to_anchor=(1, 1), fontsize='small', handlelength=0)

    if save:
         plt.savefig(f'{analysis_folder}/images/{id}_{algorithm}.png')

    plt.show()