from tkinter import Tk

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x550")
        self.title("Book Scanning Optimization")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        