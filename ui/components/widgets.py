from tkinter import Button, OptionMenu, Frame, Scrollbar, Text, VERTICAL
from ui.configs.constants import *
from ui.utils import *
from helpers.utils import plot_solution_history

class GoToPageButton(Button):
    def __init__(self, master, text, page):
        super().__init__(master=master,
                         text=text,
                         font=FONT_BUTTON_SMALL,
                         command=lambda:go_to_page(master, page)
                         )
        
class RunAgainButton(Button):
    def __init__(self, frame, page, master):
        super().__init__(master=frame,
                         text=BUTTON_RUN_AGAIN,
                         font=FONT_BUTTON_SMALL,
                         command=lambda:go_to_page(master, page)
                         )

class BackHomePageButton(Button):
    def __init__(self, frame, page, master):
        super().__init__(master=frame,
                         text=BUTTON_BACK_MAIN_PAGE,
                         font=FONT_BUTTON_SMALL,
                         command=lambda:go_to_page(master, page)
                         )

class ChooseDatasetMenu(OptionMenu):
    def __init__(self, master, var):
            super().__init__(master,
                            var,
                            *FILES)

class ChooseInitialSolutionMenu(OptionMenu):
    def __init__(self, master, var):
            super().__init__(master,
                            var,
                            *INITAL_MODES)

class ChooseMutationModeMenu(OptionMenu):
    def __init__(self, master, var):
            super().__init__(master,
                            var,
                            *MUTATION_MODES)

class ChooseCrossoverModeMenu(OptionMenu):
    def __init__(self, master, var):
            super().__init__(master,
                            var,
                            *CROSSOVER_MODES)

class RunAlgorithmButton(Button):
     def __init__(self, master, command):
        super().__init__(master=master,
                         text=RUN,
                         font=FONT_RUN,
                         command=command
                         )
        

class PlotSolutionHistoryButton(Button):
     def __init__(self, master, id, algorithm):
        super().__init__(master=master,
                         text=BUTTON_PLOT_HISTORY,
                         font=FONT_SUBTITLE,
                         command=lambda: plot_solution_history(
                              id=id,
                              algorithm=''.join(word[0] for word in algorithm.split()),
                              save=False
                          ))


class BackRunAgainButtonFrame():
    def __init__(self, master, algorithm_page, home_page):
        self.button_frame = Frame(master)
        self.button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner

        # Back to Algorithm button
        RunAgainButton(self.button_frame, algorithm_page).pack(padx=30, pady=0)

        # Back to Main Page button
        GoToPageButton(self.button_frame, BUTTON_BACK_MAIN_PAGE, home_page).pack(padx=20, pady=20)

class ScrollBarTextOutput():
    def __init__(self, master):
        self.scrollbar = Scrollbar(master, orient=VERTICAL)
        self.scrollbar.pack(side="right", fill="y")  # Pack scrollbar

        self.text_area = Text(master, wrap="word")
        self.text_area.configure(yscrollcommand=self.scrollbar.set)  # Enable vertical scrolling
        self.text_area.pack(padx=20, pady=10, fill="both", expand=True)  # Adjust packing options
        
        self.scrollbar.config(command=self.text_area.yview)  # Configure the scrollbar to control the text area's yview
    