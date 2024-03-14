from mvc.models.main import Model
from mvc.views.main import View

from .home import HomeController
from .algorithm.choose import ChooseAlgorithmController
from .algorithm.params import HCParamsController

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.choose_controller = ChooseAlgorithmController(model, view)
        self.hc_params_controller = HCParamsController(model, view)
        self.home_controller = HomeController(model, view)

    def start(self) -> None:
        self.view.start_mainloop()