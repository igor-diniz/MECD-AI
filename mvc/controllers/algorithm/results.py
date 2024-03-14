from mvc.views.main import View
from mvc.models.algorithm import Model

class AlgorithmResultsController:
    def __init__(self, view: View):
        self.dataset = view.frames["params"].file.get()