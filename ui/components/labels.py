from tkinter import Label
from ui.configs.constants import *

class MainTitleLabel(Label):
    def __init__(self, master, text=MAIN_TITLE):
        super().__init__(master,
                         text=text,
                         font=FONT_TITLE
                         )

class SubtitleLabel(Label):
    def __init__(self, master, text):
        super().__init__(master=master,
                         text=text,
                         font=FONT_SUBTITLE
                         )
        
class RegularTextLabel(Label):
    def __init__(self, master, text):
        super().__init__(master=master,
                         text=text,
                         font=FONT_TEXT
                         )

class AuthorsLabel(Label):
    def __init__(self, master):
        super().__init__(master=master,
                         text=AUTHORS_LABEL_TEXT,
                         font=FONT_AUTHORS_LABEL
                         )