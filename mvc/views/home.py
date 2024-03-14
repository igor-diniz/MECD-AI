from tkinter import Frame, Label, Button, BOTTOM

class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = Label(self,
                         text="Book Scanning Optimization",
                         font=("Arial", 18)
                         )
        self.title.pack(padx=20, pady=10)

        self.subtitle = Label(self,
                         text="Hello! Welcome to the Book Scanning Optimization UI.",
                         font=("Arial", 15)
                         )
        self.subtitle.pack(padx=20, pady=20)

        self.regular_text = Label(self,
                         text="What would you like to do?",
                         font=("Arial", 12)
                         )
        self.regular_text.pack(padx=20, pady=5)

        self.choose_alg_btn = Button(self,
                                       text = "Solve problem with a chosen optimization algorithm",
                                       font = ("Arial", 11)
                                       )
        self.choose_alg_btn.pack(padx=20, pady=10)

        self.compare_algs_btn = Button(self,
                                       text = "Compare algorithms performances",
                                       font = ("Arial", 11)
                                       )
        self.compare_algs_btn.pack(padx=20, pady=10)
        
        self.authours = Label(self,
                              text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito",
                              font=("Arial", 9)
                         )
        self.authours.pack(side=BOTTOM, pady=10)