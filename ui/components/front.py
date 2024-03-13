import tkinter as tk
from ui.configs.constants import *
from ui.utils import *
from ui.components.widgets import *
from ui.components.labels import *
from copy import deepcopy
from uuid import uuid4
from io import StringIO
import sys
from helpers.file_reader import FileReader

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x550")
        self.title(MAIN_TITLE)
        
    def homepage(self):
        HomePage(self)

    def clear_content(self):
        for widget in self.winfo_children():
                    widget.destroy()

class HomePage(App):
    def __init__(self, master):
        MainTitleLabel(master).pack(padx=20, pady=10)
        SubtitleLabel(master, HOMEPAGE_SUBTITLE).pack(padx=20, pady=20)
        RegularTextLabel(master, HOMEPAGE_TEXT).pack(padx=20, pady=5)
        
        GoToPageButton(master, BUTTON_HOMEPAGE_INDIV_ALGORITHM_TEXT, ChooseAlgorithmPage).pack(padx=20, pady=10)
        GoToPageButton(master, BUTTON_HOMEPAGE_COMPARE_TEXT, ChooseAlgorithmPage).pack(padx=20, pady=10)

        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)

class ChooseAlgorithmPage(App):
    def __init__(self, master):
        
        MainTitleLabel(master).pack(padx=20, pady=10)
       
        RegularTextLabel(master, text=SELECT_ONE_ALGORITHM_TEXT).pack(padx=20, pady=10)

        GoToPageButton(master, HC, HillClimbingPage).pack(padx=20, pady=12)
        GoToPageButton(master, SA, SimulatedAnnealingPage).pack(padx=20, pady=10)
        GoToPageButton(master, TS, TabuSearchPage).pack(padx=20, pady=10)
        GoToPageButton(master, GA, GeneticAlgorithmPage).pack(padx=20, pady=10)
        
        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)

class AlgorithmPage(App):
    def __init__(self, master, algorithm):
        MainTitleLabel(master).pack(padx=20, pady=10)
        SubtitleLabel(master, algorithm).pack(padx=20, pady=2)
        
        RegularTextLabel(master, DATASET).pack(padx=20, pady=5)
        self.file_var = tk.StringVar()
        self.file_var.set(CHOOSE_DATASET)
        ChooseDatasetMenu(master, self.file_var).pack()
        

class HillClimbingPage(AlgorithmPage):
    def __init__(self, master):
        super().__init__(master, HC)
        RegularTextLabel(master, INITIAL_SOL_MODE).pack(padx=20, pady=10)
        initial_solution_mode = tk.StringVar()
        initial_solution_mode.set(CHOOSE_MODE)
        ChooseInitialSolutionMenu(master, initial_solution_mode).pack()
        
        RegularTextLabel(master, MAX_INTER).pack(padx=20, pady=10)
        iterations_entry = tk.Entry(master)
        iterations_entry.pack()
        
        RunAlgorithmButton(master, command=lambda:go_to_algorithm_page(master=master,
                                                                       page=AlgorithmResultsPage,
                                                                       algorithm=HC,
                                                                       file=self.file_var.get(),
                                                                       solve_params=[initial_solution_mode.get(),
                                                                                     int(iterations_entry.get())]
                                                                       )
                                                              ).pack(pady=20)

        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)

class SimulatedAnnealingPage(AlgorithmPage):
    def __init__(self, master):
        super().__init__(master, SA)

        RegularTextLabel(master, INITIAL_SOL_MODE).pack(padx=20, pady=10)
        initial_solution_mode = tk.StringVar()
        initial_solution_mode.set(CHOOSE_MODE)
        ChooseInitialSolutionMenu(master, initial_solution_mode).pack()

        RegularTextLabel(master, MAX_INTER).pack(padx=20, pady=10)
        iterations_entry = tk.Entry(master)
        iterations_entry.pack()

        RegularTextLabel(master, TEMP).pack(padx=20, pady=10)
        temp_entry = tk.Entry(master)
        temp_entry.pack()

        RegularTextLabel(master, COOL_SCHED).pack(padx=20, pady=10)
        cool_sched_entry = tk.Entry(master)
        cool_sched_entry.pack()

        RunAlgorithmButton(master, command=lambda:go_to_algorithm_page(master=master,
                                                                       page=AlgorithmResultsPage,
                                                                       algorithm=SA,
                                                                       file=self.file_var.get(),
                                                                       solve_params=[initial_solution_mode.get(),
                                                                                     int(iterations_entry.get()),
                                                                                     float(temp_entry.get()),
                                                                                     float(cool_sched_entry.get())]
                                                                       )
                                                              ).pack(pady=20)
        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)

class TabuSearchPage(AlgorithmPage):
    def __init__(self, master):
        super().__init__(master, TS)

        RegularTextLabel(master, INITIAL_SOL_MODE).pack(padx=20, pady=10)
        initial_solution_mode = tk.StringVar()
        initial_solution_mode.set(CHOOSE_MODE)
        ChooseInitialSolutionMenu(master, initial_solution_mode).pack()
        
        RegularTextLabel(master, TABU_TENURE).pack(padx=20, pady=10)
        tabu_tenure_entry = tk.Entry(master)
        tabu_tenure_entry.pack()

        RegularTextLabel(master, N_NEIGHBOURS).pack(padx=20, pady=10)
        n_neighbours_entry = tk.Entry(master)
        n_neighbours_entry.pack()

        RegularTextLabel(master, MAX_INTER).pack(padx=20, pady=10)
        iterations_entry = tk.Entry(master)
        iterations_entry.pack()
        
        RunAlgorithmButton(master, command=lambda:go_to_algorithm_page(master=master,
                                                                       page=AlgorithmResultsPage,
                                                                       algorithm=TS,
                                                                       file=self.file_var.get(),
                                                                       solve_params=[initial_solution_mode.get(),
                                                                                     int(tabu_tenure_entry.get()),
                                                                                     int(n_neighbours_entry.get()),
                                                                                     int(iterations_entry.get())]
                                                                       )
                                                              ).pack(pady=20)
        
        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)

class GeneticAlgorithmPage(AlgorithmPage):
    def __init__(self, master):
        super().__init__(master, GA)

        RegularTextLabel(master, POP_SIZE).pack(padx=20, pady=10)
        pop_size_entry = tk.Entry(master)
        pop_size_entry.pack()

        RegularTextLabel(master, N_GENERATIONS).pack(padx=20, pady=10)
        n_generations_entry = tk.Entry(master)
        n_generations_entry.pack()
        
        RegularTextLabel(master, MUT_MODE).pack(padx=20, pady=10)
        mutate_var = tk.StringVar()
        mutate_var.set(CHOOSE_MODE)
        ChooseMutationModeMenu(master, mutate_var).pack()

        RegularTextLabel(master, CROSS_MODE).pack(padx=20, pady=10)
        crossover_var = tk.StringVar()
        crossover_var.set(CHOOSE_MODE)
        ChooseCrossoverModeMenu(master, crossover_var).pack()

        RunAlgorithmButton(master, command=lambda:go_to_algorithm_page(master=master,
                                                                       page=AlgorithmResultsPage,
                                                                       algorithm=GA,
                                                                       file=self.file_var.get(),
                                                                       solve_params=[int(pop_size_entry.get()),
                                                                                     int(n_generations_entry.get()),
                                                                                     mutate_var.get(),
                                                                                     crossover_var.get()]
                                                                       )
                                                              ).pack(pady=20)

        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)


class AlgorithmResultsPage(App):
    def __init__(self, master, algorithm, file, solve_params):
        id = str(uuid4())

        file_reader = FileReader()
        total_books, libraries, total_days = file_reader.read(f"data/{file}")

        original_stdout = sys.stdout  # Save original stdout for later restoration
        output_buffer = StringIO()  # Create a buffer to capture output
        sys.stdout = output_buffer  # Redirect stdout to the buffer
        
        button_frame = Frame(master)
        button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner
        
        RunAgainButton(button_frame, ChooseAlgorithmPage, master).pack(padx=30, pady=0)
        BackHomePageButton(button_frame, HomePage, master).pack(padx=20, pady=20)

        PlotSolutionHistoryButton(button_frame, id, algorithm).pack(side=tk.BOTTOM, pady=10)
        
        MainTitleLabel(master, text=algorithm).pack(padx=20, pady=10)
        subtitle = SubtitleLabel(master, RUNNING)
        subtitle.pack(padx=20, pady=2)
        scroll_text = ScrollBarTextOutput(master)

        if algorithm == HC:
            solve_hc(file, id, total_books, libraries, total_days, solve_params)
        
        if algorithm == SA:
            solve_sa(file, id, total_books, libraries, total_days, solve_params)
        
        if algorithm == TS:
            solve_ts(file, id, total_books, libraries, total_days, solve_params)

        if algorithm == GA:
            solve_ga(file, id, total_books, libraries, total_days, solve_params)
        
    

        
        subtitle.config(text="Finished execution!")
        sys.stdout = original_stdout  # Restore original stdout

        captured_output = output_buffer.getvalue()  # Get the captured output
        scroll_text.text_area.insert(tk.END, captured_output)
        scroll_text.text_area.see(tk.END)
    