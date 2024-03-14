from tkinter import Frame, Label, StringVar, Entry, Button, OptionMenu, BOTTOM
from mvc.configs import FILES

class AlgorithmParamsView(Frame):
    def __init__(self, algorithm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = Label(self,
                         text="Book Scanning Optimization",
                         font=("Arial", 18)
                         )
        self.title.pack(padx=20, pady=10)

        self.subtitle = Label(self,
                         text=algorithm,
                         font=("Arial", 15)
                         )
        self.subtitle.pack(padx=20, pady=20)

        self.choose_dataset = Label(self,
                         text="Dataset:",
                         font=("Arial", 12)
                         )
        self.choose_dataset.pack(padx=20, pady=5)

        self.file = StringVar()
        self.file.set("Choose dataset")
        self.dataset_menu = OptionMenu(self,
                                       self.file,
                                       *FILES)
        self.dataset_menu.pack()
        self.run_btn = Button(self, text="Run", font=("Arial", 14))
        self.authours = Label(self,
                              text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito",
                              font=("Arial", 9)
                         )

class HCParamsView(AlgorithmParamsView):
    def __init__(self, *args, **kwargs):
        super().__init__("Hill Climbing", *args, **kwargs)

        self.choose_init_sol = Label(self,
                         text="Initial solution generation mode:",
                         font=("Arial", 12)
                         )
        
        self.choose_init_sol.pack(padx=20, pady=5)

        self.initial_sol_mode = StringVar()
        self.initial_sol_mode.set("Choose mode")
        self.initial_sol_menu = OptionMenu(self,
                                           self.initial_sol_mode,
                                           *["Random", "Greedy"])
        self.initial_sol_menu.pack()
        
        self.choose_iter = Label(self,
                         text="Max. number of iterations:",
                         font=("Arial", 12)
                         )
        self.choose_iter.pack(padx=20, pady=10)

        self.iterations = Entry(self)
        self.iterations.pack()

        self.run_btn.pack(pady=20)
        self.authours.pack(side=BOTTOM, pady=10)

class SAParamsView(AlgorithmParamsView):
    def __init__(self, *args, **kwargs):
        super().__init__("Simulated Annealing", *args, **kwargs)

        self.choose_init_sol = Label(self,
                         text="Initial solution generation mode:",
                         font=("Arial", 12)
                         )
        
        self.choose_init_sol.pack(padx=20, pady=5)

        self.initial_sol_mode = StringVar()
        self.initial_sol_mode.set("Choose mode")
        self.initial_sol_menu = OptionMenu(self,
                                           self.initial_sol_mode,
                                           *["Random", "Greedy"])
        self.initial_sol_menu.pack()
        
        self.choose_iter = Label(self,
                         text="Max. number of iterations:",
                         font=("Arial", 12)
                         )
        self.choose_iter.pack(padx=20, pady=10)

        self.iterations = Entry(self)
        self.iterations.pack()

        self.choose_temp = Label(self,
                         text="Temperature:",
                         font=("Arial", 12)
                         )
        self.choose_temp.pack(padx=20, pady=10)

        self.temperature = Entry(self)
        self.temperature.pack()
        
        self.choose_cool_sched = Label(self,
                         text="Cooling schedule:",
                         font=("Arial", 12)
                         )
        self.choose_cool_sched.pack(padx=20, pady=10)

        self.cooling_schedule = Entry(self)
        self.cooling_schedule.pack()

        self.run_btn.pack(pady=20)
        self.authours.pack(side=BOTTOM, pady=10)

class TSParamsView(AlgorithmParamsView):
    def __init__(self, *args, **kwargs):
        super().__init__("Tabu Search", *args, **kwargs)

        self.choose_init_sol = Label(self,
                         text="Initial solution generation mode:",
                         font=("Arial", 12)
                         )
        
        self.choose_init_sol.pack(padx=20, pady=5)

        self.initial_sol_mode = StringVar()
        self.initial_sol_mode.set("Choose mode")
        self.initial_sol_menu = OptionMenu(self,
                                           self.initial_sol_mode,
                                           *["Random", "Greedy"])
        self.initial_sol_menu.pack()
        
        self.choose_tenure = Label(self,
                         text="Tabu tenure:",
                         font=("Arial", 12)
                         )
        self.choose_tenure.pack(padx=20, pady=10)

        self.tenure = Entry(self)
        self.tenure.pack()

        self.choose_nneigh = Label(self,
                         text="Number of neighbours:",
                         font=("Arial", 12)
                         )
        self.choose_nneigh.pack(padx=20, pady=10)

        self.n_neighbours = Entry(self)
        self.n_neighbours.pack()
        
        self.choose_iter = Label(self,
                         text="Max. number of iterations:",
                         font=("Arial", 12)
                         )
        self.choose_iter.pack(padx=20, pady=10)

        self.iterations = Entry(self)
        self.iterations.pack()

        self.run_btn.pack(pady=20)
        self.authours.pack(side=BOTTOM, pady=10)

class GAParamsView(AlgorithmParamsView):
    def __init__(self, *args, **kwargs):
        super().__init__("Genetic Algorithm", *args, **kwargs)

        self.choose_pop_size = Label(self,
                         text="Population size:",
                         font=("Arial", 12)
                         )
        self.choose_pop_size.pack(padx=20, pady=10)

        self.population_size = Entry(self)
        self.population_size.pack()

        self.choose_ngen = Label(self,
                         text="Number of generations:",
                         font=("Arial", 12)
                         )
        self.choose_ngen.pack(padx=20, pady=10)
        
        self.n_generations = Entry(self)
        self.n_generations.pack()

        self.choose_mutation = Label(self,
                         text="Mutation mode:",
                         font=("Arial", 12)
                         )
        self.choose_mutation.pack(padx=20, pady=10)

        self.mutation_mode = StringVar()
        self.mutation_mode.set("Choose mode")
        self.mut_mode_menu = OptionMenu(self,
                                           self.mutation_mode,
                                           *["Internal Swap",
                                             "External Swap",
                                             "Deletion",
                                             "Random"])
        self.mut_mode_menu.pack()
        
        
        self.choose_crossover = Label(self,
                         text="Crossover mode:",
                         font=("Arial", 12)
                         )
        self.choose_crossover.pack(padx=20, pady=10)

        self.crossover_mode = StringVar()
        self.crossover_mode.set("Choose mode")
        self.crossover_mode_menu = OptionMenu(self,
                                           self.crossover_mode,
                                           *["Mid Point",
                                             "Random Point"])
        self.crossover_mode_menu.pack()

        self.run_btn.pack(pady=20)
        self.authours.pack(side=BOTTOM, pady=10)