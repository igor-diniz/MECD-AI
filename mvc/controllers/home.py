from mvc.views.main import View
from mvc.models.main import Model

class HomeController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.choose_alg_btn.config(command=self.choose_algorithm)
        self.frame.compare_algs_btn.config(command=self.compare_algorithms)

    def choose_algorithm(self) -> None:
        self.view.switch("choose_algorithm")

    def compare_algorithms(self) -> None:
        self.view.switch("choose_algorithm")
