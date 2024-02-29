from tkinter import *
from io import StringIO
from helpers.file_reader import FileReader
from metaheuristics.solver import Solver
from metaheuristics.genetic_algorithm import GeneticAlgorithm
from metaheuristics.tabu_search import TabuSearchSolver
from metaheuristics.hill_climbing import HillClimbingSolver
from metaheuristics.simulated_annealing import SimulatedAnnealing
import sys
import threading
from copy import deepcopy
from uuid import uuid4

window = Tk()
window.geometry("1100x550")
window.title("Book Scanning Optimization")

#region ----- WELCOME SCREEN

# Function to create the first screen (common for algorithms 1.1-4)
def create_welcome_screen():
    # Create labels and buttons
    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)

    welcome_label = Label(window, text="Welcome to the Book Scanning Optimization UI.", font=("Arial", 15))
    welcome_label.pack(padx=20, pady=20)

    select_label = Label(window, text="What would you like to do?", font=("Arial", 12))
    select_label.pack(padx=20, pady=5)

    solve_button = Button(window,
                          text="Solve problem with a chosen optimization algorithm",
                          command=lambda: create_choose_algorithm_screen(),
                          font=("Arial", 11))
    solve_button.pack(padx=20, pady=10)

    compare_button = Button(window,
                            text="Compare algorithms performances",
                            command=lambda: create_compare_screen(),
                            font=("Arial", 11))
    compare_button.pack(padx=20, pady=10)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

#endregion
#region ----- CHOOSE ALGORITHM SCREEN

# Function to create the screen to choose the algorithm
def create_choose_algorithm_screen():
    for widget in window.winfo_children():
        widget.destroy()
    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    # Create labels, buttons, and entry fields

    mutate_mode_label = Label(window, text="Alright! Select one of the algorithms below.", font=("Arial", 11))
    mutate_mode_label.pack(padx=20, pady=10)

    hill_climbing_button = Button(window,
                          text="Hill Climbing",
                          command=lambda: create_hc_insert_params_screen(),
                          font=("Arial", 12))
    hill_climbing_button.pack(padx=20, pady=12)

    simulated_annealing_button = Button(window,
                            text="Simulated Annealing",
                            command=lambda: create_sa_insert_params_screen(),
                            font=("Arial", 12))
    simulated_annealing_button.pack(padx=20, pady=10)

    tabu_search_button = Button(window,
                            text="Tabu Search",
                            command=lambda: create_ts_insert_params_screen(),
                            font=("Arial", 12))
    tabu_search_button.pack(padx=20, pady=10)

    ga_button = Button(window,
                          text="Genetic Algorithm",
                          command=lambda: create_ga_insert_params_screen(),
                          font=("Arial", 12))
    ga_button.pack(padx=20, pady=10)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

# endregion    
#region ----- TABU SEARCH 
    #region --- INSERT TABU SEARCH PARAMS SCREEN
def create_ts_insert_params_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Tabu Search", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    file_label = Label(window, text="Dataset:", font=("Arial", 12))
    file_label.pack(padx=20, pady=5)
    file = StringVar()
    file.set("a_example.in")
    file_menu = OptionMenu(window,
                           file,
                           "a_example.in",
                           "a_example_2.in",
                           "a_example_3.in",
                           "a_example_4.in",
                           "b_read_on",
                           "c_incunabula.in",
                           "d_tough_choices.in",
                           "e_so_many_books.in",
                           "f_libraries_of_the_world")
    file_menu.pack()

    init_sol_label = Label(window, text="Initial solution generation mode",
                         font=("Arial", 12))
    init_sol_label.pack(padx=20, pady=10)
    init_sol_var = StringVar()
    init_sol_var.set("Choose mode")
    init_sol_menu = OptionMenu(window, init_sol_var, "Random", "Greedy")
    init_sol_menu.pack()

    tabu_tenure_label = Label(window, text="Tabu tenure:", font=("Arial", 12))
    tabu_tenure_label.pack(padx=20, pady=10)

    tabu_tenure_entry = Entry(window)
    tabu_tenure_entry.pack()

    neighbours_n_label = Label(window, text="Number of neighbours:", font=("Arial", 12))
    neighbours_n_label.pack(padx=20, pady=10)

    neighbours_n_entry = Entry(window)
    neighbours_n_entry.pack()

    max_iterations_label = Label(window, text="Maximum number of iterations:", font=("Arial", 12))
    max_iterations_label.pack(padx=20, pady=10)

    max_iterations_n_entry = Entry(window)
    max_iterations_n_entry.pack()
    
    run_button = Button(window, text="Run", command=lambda: run_thread(lambda: run_ts(file.get(), init_sol_var.get(), tabu_tenure_entry.get(), neighbours_n_entry.get(), max_iterations_n_entry.get())), font=("Arial", 14))  # Replace with appropriate function call to run the algorithm
    run_button.pack(padx=20, pady=20)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

    #endregion
    #region ----- TABU SEARCH RUNNING SCREEN

def run_ts(file, init_sol_var, tabu_tenure_entry, neighbours_n_entry, max_iterations_n_entry):
    for widget in window.winfo_children():
        widget.destroy()
    
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(f"data/{file}")

    original_stdout = sys.stdout  # Save original stdout for later restoration
    output_buffer = StringIO()  # Create a buffer to capture output
    sys.stdout = output_buffer  # Redirect stdout to the buffer
    
    button_frame = Frame(window)
    button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner

    # Back to Algorithm button
    back_alg_button = Button(button_frame, text="Run again with different parameters", command=lambda: back_to_page(create_ts_insert_params_screen))
    back_alg_button.pack(padx=30, pady=0)

    # Back to Main Page button
    back_button = Button(button_frame, text="Back to Main Page", command=lambda: back_to_page(create_welcome_screen))
    back_button.pack(padx=20, pady=20)

    frame_title = Label(window, text="Tabu Search", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Running...", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)
   

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.pack(side="right", fill="y")  # Pack scrollbar

    text_area = Text(window, wrap="word")
    text_area.configure(yscrollcommand=scrollbar.set)  # Enable vertical scrolling
    text_area.pack(padx=20, pady=10, fill="both", expand=True)  # Adjust packing options
    
    scrollbar.config(command=text_area.yview)  # Configure the scrollbar to control the text area's yview
    
    ts = TabuSearchSolver(total_books, libraries, total_days)
    initial_solution = ts.create_initial_solution(mode=init_sol_var)
        
    try: 
        ts.solve(
        initial_solution=initial_solution,
        tabu_tenure=int(tabu_tenure_entry),
        n_neighbours=int(neighbours_n_entry),
        max_iterations=int(max_iterations_n_entry),
        log=True,
        results_csv="analysis/ts/",
        filename=file
        )

    finally:
        frame_subtitle.config(text="Finished execution!")
        sys.stdout = original_stdout  # Restore original stdout

    captured_output = output_buffer.getvalue()  # Get the captured output
    text_area.insert(END, captured_output)
    text_area.see(END)

    #endregion
#endregion
#region ----- GENETIC ALGORITHM
    #region --- INSERT GENETIC ALGORITHM PARAMS SCREEN
def create_ga_insert_params_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Genetic Algorithm", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    file_label = Label(window, text="Dataset:", font=("Arial", 12))
    file_label.pack(padx=20, pady=5)
    file = StringVar()
    file.set("Choose dataset")
    file_menu = OptionMenu(window,
                           file,
                           "a_example.in",
                           "a_example_2.in",
                           "a_example_3.in",
                           "a_example_4.in",
                           "b_read_on",
                           "c_incunabula.in",
                           "d_tough_choices.in",
                           "e_so_many_books.in",
                           "f_libraries_of_the_world")
    file_menu.pack()

    pop_size_label = Label(window, text="Population size (min. 4):", font=("Arial", 12))
    pop_size_label.pack(padx=20, pady=10)

    pop_size_entry = Entry(window)
    pop_size_entry.pack()

    generations_n_label = Label(window, text="Number of generations:", font=("Arial", 12))
    generations_n_label.pack(padx=20, pady=10)

    generations_n_entry = Entry(window)
    generations_n_entry.pack()

    mutate_mode_label = Label(window, text="Mutation mode:", font=("Arial", 12))
    mutate_mode_label.pack(padx=20, pady=10)
    
    mutate_var = StringVar()
    mutate_var.set("Choose mode")
    mutate_menu = OptionMenu(window, mutate_var, "Swap", "Deletion", "Addition")
    mutate_menu.pack()

    crossover_mode_label = Label(window, text="Crossover mode:", font=("Arial", 12))
    crossover_mode_label.pack(padx=20, pady=10)

    crossover_var = StringVar()
    crossover_var.set("Choose mode")
    crossover_menu = OptionMenu(window, crossover_var, "Mid point", "Random point")
    crossover_menu.pack()
    
    run_button = Button(window, text="Run", command=lambda: run_thread(lambda: run_ga(file.get(), pop_size_entry.get(), generations_n_entry.get(), mutate_var.get(), crossover_var.get())), font=("Arial", 14))  # Replace with appropriate function call to run the algorithm
    run_button.pack(padx=20, pady=20)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

    #endregion
    #region --- GENETIC ALGORITHM RUNNING SCREEN
def run_ga(file, pop_size_entry, generations_n_entry, mutate_var, crossover_var):
    for widget in window.winfo_children():
        widget.destroy()
    
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(f"data/{file}")

    original_stdout = sys.stdout  # Save original stdout for later restoration
    output_buffer = StringIO()  # Create a buffer to capture output
    sys.stdout = output_buffer  # Redirect stdout to the buffer

    button_frame = Frame(window)
    button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner

    # Back to Algorithm button
    back_alg_button = Button(button_frame, text="Run again with different parameters", command=lambda: back_to_page(create_ga_insert_params_screen))
    back_alg_button.pack(padx=30, pady=0)

    # Back to Main Page button
    back_button = Button(button_frame, text="Back to Main Page", command=lambda: back_to_page(create_welcome_screen))
    back_button.pack(padx=20, pady=20)

    frame_title = Label(window, text="Genetic Algorithm", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Running...", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.pack(side="right", fill="y")  # Pack scrollbar

    text_area = Text(window, wrap="word")
    text_area.configure(yscrollcommand=scrollbar.set)  # Enable vertical scrolling
    text_area.pack(padx=20, pady=10, fill="both", expand=True)  # Adjust packing options
    
    scrollbar.config(command=text_area.yview)  # Configure the scrollbar to control the text area's yview
    
    ga = GeneticAlgorithm(total_books, libraries, total_days)
    
    try: 
        ga.solve(
        population_size=int(pop_size_entry),
        n_generations=int(generations_n_entry),
        mutate_mode=mutate_var,
        crossover_mode=crossover_var,
        results_csv="analysis/ga/",
        filename=file
        )

    finally:
        frame_subtitle.config(text="Finished execution!")
        sys.stdout = original_stdout  # Restore original stdout

    captured_output = output_buffer.getvalue()  # Get the captured output
    text_area.insert(END, captured_output)
    text_area.see(END)

    #endregion
#endregion
#region ----- HILL CLIMBING 
    #region --- INSERT HILL CLIMBING PARAMS SCREEN
def create_hc_insert_params_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Hill Climbing", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    file_label = Label(window, text="Dataset:", font=("Arial", 12))
    file_label.pack(padx=20, pady=5)
    file = StringVar()
    file.set("a_example.in")
    file_menu = OptionMenu(window,
                           file,
                           "a_example.in",
                           "a_example_2.in",
                           "a_example_3.in",
                           "a_example_4.in",
                           "b_read_on",
                           "c_incunabula.in",
                           "d_tough_choices.in",
                           "e_so_many_books.in",
                           "f_libraries_of_the_world")
    file_menu.pack()

    init_sol_label = Label(window, text="Initial solution generation mode",
                         font=("Arial", 12))
    init_sol_label.pack(padx=20, pady=10)
    init_sol_var = StringVar()
    init_sol_var.set("Choose mode")
    init_sol_menu = OptionMenu(window, init_sol_var, "Random", "Greedy")
    init_sol_menu.pack()
    
    max_iterations_label = Label(window, text="Maximum number of iterations:", font=("Arial", 12))
    max_iterations_label.pack(padx=20, pady=10)

    max_iterations_n_entry = Entry(window)
    max_iterations_n_entry.pack()
    
    run_button = Button(window, text="Run", command=lambda: run_thread(lambda: run_hc(file.get(), init_sol_var.get(), max_iterations_n_entry.get())), font=("Arial", 14))  # Replace with appropriate function call to run the algorithm
    run_button.pack(padx=20, pady=20)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

    #endregion
    #region ----- HILL CLIMBING RUNNING SCREEN

def run_hc(file, init_sol_var, max_iterations_n_entry):
    for widget in window.winfo_children():
        widget.destroy()
    
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(f"data/{file}")

    original_stdout = sys.stdout  # Save original stdout for later restoration
    output_buffer = StringIO()  # Create a buffer to capture output
    sys.stdout = output_buffer  # Redirect stdout to the buffer

    button_frame = Frame(window)
    button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner

    # Back to Algorithm button
    back_alg_button = Button(button_frame, text="Run again with different parameters", command=lambda: back_to_page(create_hc_insert_params_screen))
    back_alg_button.pack(padx=30, pady=0)

    # Back to Main Page button
    back_button = Button(button_frame, text="Back to Main Page", command=lambda: back_to_page(create_welcome_screen))
    back_button.pack(padx=20, pady=20)

    frame_title = Label(window, text="Hill Climbing", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Running...", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.pack(side="right", fill="y")  # Pack scrollbar

    text_area = Text(window, wrap="word")
    text_area.configure(yscrollcommand=scrollbar.set)  # Enable vertical scrolling
    text_area.pack(padx=20, pady=10, fill="both", expand=True)  # Adjust packing options
    
    scrollbar.config(command=text_area.yview)  # Configure the scrollbar to control the text area's yview
    
    hc = HillClimbingSolver(total_books, libraries, total_days)
    initial_solution = hc.create_initial_solution(mode=init_sol_var)
    
    try: 
        hc.solve(
            initial_solution=initial_solution,
            num_iterations=int(max_iterations_n_entry),
            results_csv='analysis/hc/',
            filename=file,
            log=True)

    finally:
        frame_subtitle.config(text="Finished execution!")
        sys.stdout = original_stdout  # Restore original stdout

    captured_output = output_buffer.getvalue()  # Get the captured output
    text_area.insert(END, captured_output)
    text_area.see(END)

    #endregion
#endregion
#region ----- SIMULATED ANNEALING 
    #region --- INSERT SIMULATED ANNEALING PARAMS SCREEN
def create_sa_insert_params_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Simulated Annealing", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    file_label = Label(window, text="Dataset:", font=("Arial", 12))
    file_label.pack(padx=20, pady=5)
    file = StringVar()
    file.set("a_example.in")
    file_menu = OptionMenu(window,
                           file,
                           "a_example.in",
                           "a_example_2.in",
                           "a_example_3.in",
                           "a_example_4.in",
                           "b_read_on",
                           "c_incunabula.in",
                           "d_tough_choices.in",
                           "e_so_many_books.in",
                           "f_libraries_of_the_world")
    file_menu.pack()

    init_sol_label = Label(window, text="Initial solution generation mode",
                         font=("Arial", 12))
    init_sol_label.pack(padx=20, pady=10)
    init_sol_var = StringVar()
    init_sol_var.set("Choose mode")
    init_sol_menu = OptionMenu(window, init_sol_var, "Random", "Greedy")
    init_sol_menu.pack()
    
    max_iterations_label = Label(window, text="Maximum number of iterations:", font=("Arial", 12))
    max_iterations_label.pack(padx=20, pady=10)

    max_iterations_n_entry = Entry(window)
    max_iterations_n_entry.pack()

    temperature_label = Label(window, text="Temperature:", font=("Arial", 12))
    temperature_label.pack(padx=20, pady=10)

    temperature_entry = Entry(window)
    temperature_entry.pack()
    
    cooling_schedule_label = Label(window, text="Cooling schedule:", font=("Arial", 12))
    cooling_schedule_label.pack(padx=20, pady=10)

    cooling_schedule_entry = Entry(window)
    cooling_schedule_entry.pack()
    
    run_button = Button(window, text="Run", command=lambda: run_thread(lambda: run_sa(file.get(), init_sol_var.get(),
                                                                                      max_iterations_n_entry.get(),
                                                                                      temperature_entry.get(),
                                                                                      cooling_schedule_entry.get())), font=("Arial", 14))  # Replace with appropriate function call to run the algorithm
    run_button.pack(padx=20, pady=20)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

    #endregion
    #region ----- SIMULATED ANNEALING RUNNING SCREEN

def run_sa(file, init_sol_var, max_iterations_n_entry, temperature_entry, cooling_schedule_entry):
    for widget in window.winfo_children():
        widget.destroy()
    
    file_reader = FileReader()
    total_books, libraries, total_days = file_reader.read(f"data/{file}")

    original_stdout = sys.stdout  # Save original stdout for later restoration
    output_buffer = StringIO()  # Create a buffer to capture output
    sys.stdout = output_buffer  # Redirect stdout to the buffer

    button_frame = Frame(window)
    button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner

    # Back to Algorithm button
    back_alg_button = Button(button_frame, text="Run again with different parameters", command=lambda: back_to_page(create_sa_insert_params_screen))
    back_alg_button.pack(padx=30, pady=0)

    # Back to Main Page button
    back_button = Button(button_frame, text="Back to Main Page", command=lambda: back_to_page(create_welcome_screen))
    back_button.pack(padx=20, pady=20)

    frame_title = Label(window, text="Simulated Annealing", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Running...", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    scrollbar = Scrollbar(window, orient=VERTICAL)
    scrollbar.pack(side="right", fill="y")  # Pack scrollbar

    text_area = Text(window, wrap="word")
    text_area.configure(yscrollcommand=scrollbar.set)  # Enable vertical scrolling
    text_area.pack(padx=20, pady=10, fill="both", expand=True)  # Adjust packing options
    
    scrollbar.config(command=text_area.yview)  # Configure the scrollbar to control the text area's yview
    
    sa = SimulatedAnnealing(total_books, libraries, total_days)
    initial_solution = sa.create_initial_solution(mode=init_sol_var)
    
    try: 
        sa.solve(
            initial_solution=initial_solution,
            num_iterations=int(max_iterations_n_entry),
            T=float(temperature_entry),
            cooling_schedule=float(cooling_schedule_entry),
            log=True,
            results_csv="analysis/sa/",
            filename=file)

    finally:
        frame_subtitle.config(text="Finished execution!")
        sys.stdout = original_stdout  # Restore original stdout

    captured_output = output_buffer.getvalue()  # Get the captured output
    text_area.insert(END, captured_output)
    text_area.see(END)

    #endregion
#endregion    
#region ----- COMPARE ALGORITHMS SCREEN

def running_algorithms_screen(file,
                              init_sol_var,
                              hc_var,
                              hc_max_iterations_n_entry,
                              sa_var,
                              sa_max_iterations_n_entry,
                              temperature_entry,
                              cooling_schedule_entry,
                              ts_var,
                              tabu_tenure_entry,
                              neighbours_n_entry,
                              ts_max_iterations_n_entry,
                              ga_var,
                              pop_size_entry,
                              generations_n_entry,
                              mutate_var,
                              crossover_var):
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Comparing Algorithms...", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)
    
    #region Run Selected Algorithms
    filename = file
    file_reader = FileReader()

    # Common inputs
    total_books, libraries, total_days = file_reader.read(f"data/{filename}")
    initial_solution = Solver(total_books, libraries, total_days).create_initial_solution(mode=init_sol_var)
    uuid = uuid4()
    
    if hc_var == 1:
        hc = HillClimbingSolver(total_books, deepcopy(libraries), total_days)
        num_iterations = hc_max_iterations_n_entry
        hc.solve(
            initial_solution=deepcopy(initial_solution),
            num_iterations=int(num_iterations),
            results_csv='analysis/hc/',
            filename=file,
            log=True)
    
    if sa_var == 1:  
        sa = SimulatedAnnealing(total_books, deepcopy(libraries), total_days)
        sa.solve(
            initial_solution=deepcopy(initial_solution),
            num_iterations=int(sa_max_iterations_n_entry),
            T=float(temperature_entry),
            cooling_schedule=float(cooling_schedule_entry),
            log=True,
            results_csv="analysis/sa/",
            filename=file)

    if ts_var == 1:
        ts = TabuSearchSolver(total_books, deepcopy(libraries), total_days)
        ts.solve(
            initial_solution=deepcopy(initial_solution),
            tabu_tenure=int(tabu_tenure_entry),
            n_neighbours=int(neighbours_n_entry),
            max_iterations=int(ts_max_iterations_n_entry),
            log=True,
            results_csv="analysis/ts/",
            filename=file
            )

    if ga_var == 1:
        ga = GeneticAlgorithm(total_books, deepcopy(libraries), total_days)
        ga.solve(
            population_size=int(pop_size_entry),
            n_generations=int(generations_n_entry),
            mutate_mode=mutate_var,
            crossover_mode=crossover_var,
            results_csv="analysis/ga/",
            filename=file
        )

        frame_subtitle.config(text="Finished Algorithms Execution!")

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

def create_compare_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Compare Algorithms", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    authours_label = Label(window, text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito", font=("Arial", 9))
    authours_label.pack(side=BOTTOM, pady=20)

    # Create compare button frame
    button_frame = Frame(window)
    button_frame.pack(side=BOTTOM)

    # Create common parameters frame
    common_frame = Frame(window)
    common_frame.pack(side=TOP, pady=20)

    file_label = Label(common_frame, text="Dataset:", font=("Arial", 12))
    file_label.pack(side=LEFT, padx=20, pady=5)
    file = StringVar()
    file.set("a_example.in")
    file_menu = OptionMenu(common_frame,
                           file,
                           "a_example.in",
                           "a_example_2.in",
                           "a_example_3.in",
                           "a_example_4.in",
                           "b_read_on",
                           "c_incunabula.in",
                           "d_tough_choices.in",
                           "e_so_many_books.in",
                           "f_libraries_of_the_world")
    file_menu.pack(side=LEFT)

    init_sol_label = Label(common_frame, text="Initial solution generation mode:",
                         font=("Arial", 12))
    init_sol_label.pack(side=LEFT, padx=40, pady=10)
    init_sol_var = StringVar()
    init_sol_var.set("Choose mode")
    init_sol_menu = OptionMenu(common_frame, init_sol_var, "Random", "Greedy")
    init_sol_menu.pack(side=LEFT)


    frames = []
    for _ in range(5):
        frame = Frame(window, padx=10, pady=10)
        frame.pack(side=LEFT, padx=10, fill=Y)
        frames.append(frame)

    # Compare button
    compare_button = Button(button_frame,
                            text="Compare",
                            command=lambda: running_algorithms_screen(
                                file.get(),
                                init_sol_var.get(),
                                hc_var.get(),
                                hc_max_iterations_n_entry.get(),
                                sa_var.get(),
                                sa_max_iterations_n_entry.get(),
                                temperature_entry.get(),
                                cooling_schedule_entry.get(),
                                ts_var.get(),
                                tabu_tenure_entry.get(),
                                neighbours_n_entry.get(),
                                ts_max_iterations_n_entry.get(),
                                ga_var.get(),
                                pop_size_entry.get(),
                                generations_n_entry.get(),
                                mutate_var.get(),
                                crossover_var.get()
                            ),
                            font=("Arial", 15))
    compare_button.pack(padx=20)

    #region HC PARAMS
    hc_var = IntVar(value=1)  # Initialize as selected
    hc_check = Checkbutton(frames[1], text="Hill Climbing", variable=hc_var, font=("Arial", 12))
    hc_check.pack(anchor=NW, padx=5, pady=5)

    hc_max_iterations_label = Label(frames[1], text="Maximum number of iterations:", font=("Arial", 10))
    hc_max_iterations_label.pack(anchor=NW, padx=5, pady=5)

    hc_max_iterations_n_entry = Entry(frames[1])
    hc_max_iterations_n_entry.pack(anchor=NW, padx=5, pady=5)
    #endregion
        
    #region SA PARAMS
    sa_var = IntVar(value=1)  # Initialize as selected
    sa_check = Checkbutton(frames[2], text="Simulated Annealing", variable=sa_var, font=("Arial", 12))
    sa_check.pack(anchor=NW, padx=5, pady=5)
    
    sa_max_iterations_label = Label(frames[2], text="Maximum number of iterations:", font=("Arial", 10))
    sa_max_iterations_label.pack(anchor=NW, padx=5, pady=5)

    sa_max_iterations_n_entry = Entry(frames[2])
    sa_max_iterations_n_entry.pack(anchor=NW, padx=5, pady=5)

    temperature_label = Label(frames[2], text="Temperature:", font=("Arial", 10))
    temperature_label.pack(anchor=NW, padx=5, pady=5)

    temperature_entry = Entry(frames[2])
    temperature_entry.pack(anchor=NW, padx=5, pady=5)
    
    cooling_schedule_label = Label(frames[2], text="Cooling schedule:", font=("Arial", 10))
    cooling_schedule_label.pack(anchor=NW, padx=5, pady=5)

    cooling_schedule_entry = Entry(frames[2])
    cooling_schedule_entry.pack(anchor=NW, padx=5, pady=5)
    #endregion

    #region TS PARAMS
    ts_var = IntVar(value=1)  # Initialize as selected
    ts_check = Checkbutton(frames[3], text="Tabu Search", variable=ts_var, font=("Arial", 12))
    ts_check.pack(anchor=NW, padx=5, pady=5)

    tabu_tenure_label = Label(frames[3], text="Tabu tenure:", font=("Arial", 10))
    tabu_tenure_label.pack(anchor=NW, padx=15, pady=2)

    tabu_tenure_entry = Entry(frames[3])
    tabu_tenure_entry.pack(anchor=NW, padx=15, pady=2)

    neighbours_n_label = Label(frames[3], text="Number of neighbours:", font=("Arial", 10))
    neighbours_n_label.pack(anchor=NW, padx=15, pady=2)

    neighbours_n_entry = Entry(frames[3])
    neighbours_n_entry.pack(anchor=NW, padx=15, pady=2)

    ts_max_iterations_label = Label(frames[3], text="Maximum number of iterations:", font=("Arial", 10))
    ts_max_iterations_label.pack(anchor=NW, padx=15, pady=2)

    ts_max_iterations_n_entry = Entry(frames[3])
    ts_max_iterations_n_entry.pack(anchor=NW, padx=15, pady=2)
    #endregion

    #region GA PARAMS
    ga_var = IntVar(value=1)  # Initialize as selected
    ga_check = Checkbutton(frames[4], text="Genetic Algorithm", variable=ga_var, font=("Arial", 12))
    ga_check.pack(anchor=NW, padx=15, pady=2)

    pop_size_label = Label(frames[4], text="Population size (min. 4):", font=("Arial", 10))
    pop_size_label.pack(anchor=NW, padx=15, pady=2)

    pop_size_entry = Entry(frames[4])
    pop_size_entry.pack(anchor=NW, padx=15, pady=2)

    generations_n_label = Label(frames[4], text="Number of generations:", font=("Arial", 10))
    generations_n_label.pack(anchor=NW, padx=15, pady=2)

    generations_n_entry = Entry(frames[4])
    generations_n_entry.pack(anchor=NW, padx=15, pady=2)

    mutate_mode_label = Label(frames[4], text="Mutation mode:", font=("Arial", 10))
    mutate_mode_label.pack(anchor=NW, padx=15, pady=2)
    
    mutate_var = StringVar()
    mutate_var.set("Choose mode")
    mutate_menu = OptionMenu(frames[4], mutate_var, "Swap", "Deletion", "Addition")
    mutate_menu.pack(anchor=NW, padx=15, pady=2)

    crossover_mode_label = Label(frames[4], text="Crossover mode:", font=("Arial", 10))
    crossover_mode_label.pack(anchor=NW, padx=15, pady=2)

    crossover_var = StringVar()
    crossover_var.set("Choose mode")
    crossover_menu = OptionMenu(frames[4], crossover_var, "Mid point", "Random point")
    crossover_menu.pack(anchor=NW, padx=15, pady=2)
    #endregion


#endregion
#region ----- Others:Utils button functions
def run_thread(function):
    threading.Thread(target=function).start()

def back_to_page(function):
    for widget in window.winfo_children():
        widget.destroy()
    function()

#endregion