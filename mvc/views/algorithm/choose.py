from tkinter import Frame, Label, Button, BOTTOM

class ChooseAlgorithmView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = Label(self,
                         text="Book Scanning Optimization",
                         font=("Arial", 18)
                         )
        self.title.pack(padx=20, pady=10)

        self.regular_text = Label(self,
                         text="Alright! Select one of the algorithms below.",
                         font=("Arial", 12)
                         )
        self.regular_text.pack(padx=20, pady=10)

        self.hc_btn = Button(self, text="Hill Climbing", font=("Arial", 11))
        self.hc_btn.pack(padx=20, pady=12)

        self.sa_btn = Button(self, text="Simulated Annealing", font=("Arial", 11))
        self.sa_btn.pack(padx=20, pady=10)

        self.ts_btn = Button(self, text="Tabu Search", font=("Arial", 11))
        self.ts_btn.pack(padx=20, pady=10)

        self.ga_btn = Button(self, text="Genetic Algorithm", font=("Arial", 11))
        self.ga_btn.pack(padx=20, pady=10)

        self.authours = Label(self,
                              text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito",
                              font=("Arial", 9)
                         )
        self.authours.pack(side=BOTTOM, pady=10)
