from tkinter import *

# Function to switch between screens
def switch_screen(screen_number):
    # Clear the current screen
    for widget in window.winfo_children():
        widget.destroy()

    # Create widgets for the given screen
    if screen_number == "choose_algorithm":
        create_choose_algorithm_screen()
    elif screen_number == "compare":
        create_compare_screen()
    elif screen_number == "log":
        create_log_screen()

# Function to create the first screen (common for algorithms 1.1-4)
def create_screen_1():
    # Create labels and buttons
    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)


    welcome_label = Label(window, text="Hello! Welcome to the Book Scanning Optimization UI. What would you like to do?", font=("Arial", 12))
    welcome_label.pack(padx=20, pady=20)

    solve_button = Button(window,
                          text="Solve problem with a chosen optimization algorithm",
                          command=lambda: switch_screen("choose_algorithm"),
                          font=("Arial", 11))
    solve_button.pack(padx=20, pady=20)

    compare_button = Button(window,
                            text="Compare algorithms performances",
                            command=lambda: switch_screen("compare"),
                            font=("Arial", 11))
    compare_button.pack()

# Function to create the screen to choose the algorithm
def create_choose_algorithm_screen():
    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    # Create labels, buttons, and entry fields
    choose_label = Label(window, text="Alright! Please, choose an algorithm.",
                         font=("Arial", 11))
    choose_label.pack()

    #algorithm_var = StringVar()
    #algorithm_menu = OptionMenu(window, algorithm_var, "Hill Climbing", "Simulated Annealing", "Tabu Search", "Genetic Algorithm")
    #algorithm_menu.pack()

    hill_climbing_button = Button(window,
                          text="Hill Climbing",
                          command=lambda: create_ga_insert_params_screen(),
                          font=("Arial", 12))
    hill_climbing_button.pack(padx=20, pady=12)

    simulated_annealing_button = Button(window,
                            text="Simulated Annealing",
                            command=lambda: switch_screen("compare"),
                            font=("Arial", 12))
    simulated_annealing_button.pack(padx=20, pady=10)

    tabu_search_button = Button(window,
                            text="Tabu Search",
                            command=lambda: switch_screen("compare"),
                            font=("Arial", 12))
    tabu_search_button.pack(padx=20, pady=10)

    ga_button = Button(window,
                          text="Genetic Algorithm",
                          command=lambda: create_ga_insert_params_screen(),
                          font=("Arial", 12))
    ga_button.pack(padx=20, pady=10)
    # ... Add more parameter entry fields as needed based on the chosen algorithm


def create_ga_insert_params_screen():
    for widget in window.winfo_children():
        widget.destroy()

    frame_title = Label(window, text="Book Scanning Optimization", font=("Arial", 18))
    frame_title.pack(padx=20, pady=10)
    frame_subtitle = Label(window, text="Genetic Algorithm", font=("Arial", 16))
    frame_subtitle.pack(padx=20, pady=2)

    pop_size_label = Label(window, text="Population size:", font=("Arial", 12))
    pop_size_label.pack(padx=20, pady=10)

    pop_size_entry = Entry(window)
    pop_size_entry.pack()

    generations_n_label = Label(window, text="Number of generations:", font=("Arial", 12))
    generations_n_label.pack(padx=20, pady=10)

    generations_n_entry = Entry(window)
    generations_n_entry.pack()

    mutate_mode_label = Label(window, text="Mutation mode (swap, deletion or addition):", font=("Arial", 12))
    mutate_mode_label.pack(padx=20, pady=10)

    mutate_mode_entry = Entry(window)
    mutate_mode_entry.pack()

    crossover_mode_label = Label(window, text="Crossover mode (mid or random point):", font=("Arial", 12))
    crossover_mode_label.pack(padx=20, pady=10)

    crossover_mode_entry = Entry(window)
    crossover_mode_entry.pack()
    
    run_button = Button(window, text="Run", command=lambda: switch_screen("1.1-4"), font=("Arial", 14))  # Replace with appropriate function call to run the algorithm
    run_button.pack(padx=20, pady=10)

    # ... Add more parameter entry fields as needed based on the chosen algorithm

# Function to create the screen to compare algorithms
def create_compare_screen():
    # Create labels and buttons
    compare_label = Label(window, text="Compare algorithms")
    compare_label.pack()

    # ... Add widgets to compare algorithms

# Function to create the screen to show the log
def create_log_screen():
    # Create labels and text area to display log
    log_label = Label(window, text="Log")
    log_label.pack()

    log_text_area = Text(window)
    log_text_area.pack()

# Create the main window
window = Tk()
window.geometry("800x500")
window.title("Book Scanning Optimization")

# Create the starting screen
create_screen_1()

# Run the main loop
window.mainloop()
