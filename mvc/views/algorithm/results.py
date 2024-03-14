from tkinter import Frame, Label, Button, BOTTOM, Scrollbar, Text, VERTICAL
from mvc.views.root import Root
import sys
from io import StringIO

class AlgorithmResultsView(Frame):
    def __init__(self, algorithm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = sys.stdout  # Save original stdout for later restoration
        self.output_buffer = StringIO()  # Create a buffer to capture output
        sys.stdout = self.output_buffer  # Redirect stdout to the buffer
        
        self.button_frame = Frame(self)
        self.button_frame.pack(side="bottom", anchor="c")  # Align the frame to the top-right corner

        self.run_again_btn = Button(self.button_frame,
                                    text="Run again with different parameters",
                                    font=("Arial", 11))
        self.run_again_btn.pack(padx=30, pady=0)

        self.homepage_btn = Button(self.button_frame,
                                    text="Back to home page",
                                    font=("Arial", 11))
        self.homepage_btn.pack(padx=30, pady=20)

        self.plot_btn = Button(self, text="Plot solution history", font=("Arial", 11))
        self.plot_btn.pack(side=BOTTOM, pady=10)

        self.title = Label(self,
                         text=algorithm,
                         font=("Arial", 18)
                         )
        self.title.pack(padx=20, pady=10)

        self.status = Label(self,
                         text="Running...",
                         font=("Arial", 12)
                         )
        self.status.pack(padx=20, pady=2)
        #self.scrollbar = Scrollbar(Root(), VERTICAL)
        #self.scrollbar.pack(side="right", fill="y")  # Pack scrollbar

        self.text_area = Text(self, wrap="word")
        #self.text_area.configure(yscrollcommand=self.scrollbar.set)  # Enable vertical scrolling
        self.text_area.pack(padx=20, pady=10, fill="both", expand=True)  # Adjust packing options
        
        #self.scrollbar.config(command=self.text_area.yview)  # Configure the scrollbar to control the text area's yview
    

        self.authours = Label(self,
                              text="Developed by Ingrid Diniz, Igor Diniz and Paula Ito",
                              font=("Arial", 9)
                         )
        self.authours.pack(side=BOTTOM, pady=10)
