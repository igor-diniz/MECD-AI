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
        
        GoToPageButton(master, BUTTON_HOMEPAGE_INDIV_ALGORITHM_TEXT, CompareAlgorithmsPage).pack(padx=20, pady=10)
        GoToPageButton(master, BUTTON_HOMEPAGE_COMPARE_TEXT, CompareAlgorithmsPage).pack(padx=20, pady=10)

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
    
class CompareAlgorithmsPage(App):
    def __init__(self, master):#, algorithm, file, solve_params):
        
        MainTitleLabel(master, MAIN_TITLE).pack(padx=20, pady=10)
        SubtitleLabel(master, BUTTON_HOMEPAGE_COMPARE_TEXT)

        AuthorsLabel(master).pack(side=tk.BOTTOM, pady=10)

        # Create compare button frame
        button_frame = Frame(master)
        button_frame.pack(side=tk.BOTTOM)

        # Create common parameters frame
        common_frame = Frame(master)
        common_frame.pack(side=tk.TOP, pady=20)
        
        RegularTextLabel(master, DATASET).pack(padx=20, pady=5)
        self.file_var = tk.StringVar()
        self.file_var.set(CHOOSE_DATASET)
        ChooseDatasetMenu(master, self.file_var).pack(side=tk.LEFT)

        RegularTextLabel(master, INITIAL_SOL_MODE).pack(padx=20, pady=10)
        initial_solution_mode = tk.StringVar()
        initial_solution_mode.set(CHOOSE_MODE)
        ChooseInitialSolutionMenu(master, initial_solution_mode).pack(side=tk.LEFT)

        frames = []

        for _ in range(5):
            frame = Frame(master, padx=10, pady=10)
            frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)
            frames.append(frame)
        
        RunAlgorithmButton(button_frame,
                           COMPARE_TEXT,
                           lambda:print("hi")
                           #command=lambda:go_to_compare_results_page(
                           #    master,
                           #    CompareAlgorithmsResultsPage,
                           #    self.file_var.get(),
                           #    [hc_var.get(),
                           #     sa_var.get(),
                           #     ts_var.get(),
                           #     ga_var.get()],
                           #    [hc_solve_params,
                           #     sa_solve_params,
                           #     ts_solve_params,
                           #     ga_solve_params]
                           #)
                           ).pack(padx=20, pady=0)
        
        id = str(uuid4())

        # HC params
        hc_var = tk.IntVar(value=1)  # Initialize as selected
        AlgorithmCheckbutton(frames[1], HC, hc_var).pack(anchor=tk.NW, padx=5, pady=5)
  
        RegularTextLabel(frames[1], MAX_INTER).pack(padx=20, pady=10)
        iterations_entry = tk.Entry(frames[1])
        iterations_entry.pack()

        #hc_solve_params = [initial_solution_mode.get(), int(iterations_entry.get())]
        
        # SA params
        sa_var = tk.IntVar(value=1)  # Initialize as selected
        AlgorithmCheckbutton(frames[2], SA, sa_var).pack(anchor=tk.NW, padx=5, pady=5)
        RegularTextLabel(frames[2], MAX_INTER).pack(anchor=tk.NW, padx=5, pady=5)
        iterations_entry = tk.Entry(frames[2])
        iterations_entry.pack(anchor=tk.NW, padx=5, pady=5)

        RegularTextLabel(frames[2], TEMP).pack(anchor=tk.NW, padx=5, pady=5)
        temp_entry = tk.Entry(frames[2])
        temp_entry.pack(anchor=tk.NW, padx=5, pady=5)

        RegularTextLabel(frames[2], COOL_SCHED).pack(anchor=tk.NW, padx=5, pady=5)
        cool_sched_entry = tk.Entry(frames[2])
        cool_sched_entry.pack(anchor=tk.NW, padx=5, pady=5)

        #sa_solve_params = [initial_solution_mode.get(),
        #                  int(iterations_entry.get()),
        #                  float(temp_entry.get()),
        #                  float(cool_sched_entry.get())]

        # TS params
        ts_var = tk.IntVar(value=1)  # Initialize as selected
        AlgorithmCheckbutton(frames[3], TS, ts_var).pack(anchor=tk.NW, padx=5, pady=5)
        
        RegularTextLabel(frames[3], TABU_TENURE).pack(anchor=tk.NW, padx=15, pady=2)
        tabu_tenure_entry = tk.Entry(frames[3])
        tabu_tenure_entry.pack(anchor=tk.NW, padx=15, pady=2)

        RegularTextLabel(frames[3], N_NEIGHBOURS).pack(anchor=tk.NW, padx=15, pady=2)
        n_neighbours_entry = tk.Entry(frames[3])
        n_neighbours_entry.pack(anchor=tk.NW, padx=15, pady=2)

        RegularTextLabel(frames[3], MAX_INTER).pack(anchor=tk.NW, padx=15, pady=2)
        iterations_entry = tk.Entry(frames[3])
        iterations_entry.pack(anchor=tk.NW, padx=15, pady=2)

        #ts_solve_params = [initial_solution_mode.get(),
        #                  int(tabu_tenure_entry.get()),
        #                  int(n_neighbours_entry.get()),
        #                  int(iterations_entry.get())]

        # GA params
        ga_var = tk.IntVar(value=1)  # Initialize as selected
        AlgorithmCheckbutton(frames[4], GA, ga_var).pack(anchor=tk.NW, padx=15, pady=2)

        RegularTextLabel(master, POP_SIZE).pack(anchor=tk.NW, padx=15, pady=2)
        pop_size_entry = tk.Entry(master)
        pop_size_entry.pack(anchor=tk.NW, padx=15, pady=2)

        RegularTextLabel(master, N_GENERATIONS).pack(anchor=tk.NW, padx=15, pady=2)
        n_generations_entry = tk.Entry(master)
        n_generations_entry.pack(anchor=tk.NW, padx=15, pady=2)
        
        RegularTextLabel(master, MUT_MODE).pack(anchor=tk.NW, padx=15, pady=2)
        mutate_var = tk.StringVar()
        mutate_var.set(CHOOSE_MODE)
        ChooseMutationModeMenu(master, mutate_var).pack(anchor=tk.NW, padx=15, pady=2)

        RegularTextLabel(master, CROSS_MODE).pack(anchor=tk.NW, padx=15, pady=2)
        crossover_var = tk.StringVar()
        crossover_var.set(CHOOSE_MODE)
        ChooseCrossoverModeMenu(master, crossover_var).pack(anchor=tk.NW, padx=15, pady=2)

        #ga_solve_params = [int(pop_size_entry.get()),
        #                   int(n_generations_entry.get()),
        #                   mutate_var.get(),
        #                   crossover_var.get()]
        
class RunningAlgorithmsPage(App):
    def __init__(self, master, file, check_alg, solve_params):
            id = str(uuid4())
            MainTitleLabel(master, text=MAIN_TITLE).pack(padx=20, pady=10)
            subtitle = SubtitleLabel(master, RUNNING)
            subtitle.pack(padx=20, pady=2)

            filename = file
            file_reader = FileReader()
            total_books, libraries, total_days = file_reader.read(f"data/{filename}")
            initial_solution = Solver(total_books, libraries, total_days).create_initial_solution(mode=init_sol_var)
    
class CompareAlgorithmsResultsPage(App):
    def __init__(self, master, file, check_alg, solve_params):
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

        