from mvc.views.main import View
from mvc.models.algorithm import HCModel
from uuid import uuid4

class ParamsController:
    def __init__(self, view: View):
        self.dataset = view.frames["params"].file.get()

class HCParamsController:
    def __init__(self, model: HCModel, view: View) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.frame = self.view.frames["hc_params"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.run_btn.config(command=self.run_hc)

    def show_results(self) -> None:
        self.view.switch("alg_results")

    def run_hc(self) -> None:
        self.show_results()
        id = str(uuid4())
        file = (f"data/{self.frame.file.get()}")
        params = [self.frame.initial_sol_mode.get(),
                  int(self.frame.iterations.get())]
        self.model.hc.solve(file, id, params)


#class SAParamsController:
#    def __init__(self, model: Model, view: View) -> None:
#        self.model = model
#        self.view = view
#        self.frame = self.view.frames["sa_params"]
#        self._bind()
#
#    def _bind(self) -> None:
#        """Binds controller functions with respective buttons in the view"""
#        self.frame.run_btn.config(command=self.choose_algorithm)
#
#    def choose_algorithm(self) -> None:
#        self.view.switch("choose_algorithm")
#
#class TSParamsController:
#    def __init__(self, model: Model, view: View) -> None:
#        self.model = model
#        self.view = view
#        self.frame = self.view.frames["ts_params"]
#        self._bind()
#
#    def _bind(self) -> None:
#        """Binds controller functions with respective buttons in the view"""
#        self.frame.run_btn.config(command=self.choose_algorithm)
#
#    def choose_algorithm(self) -> None:
#        self.view.switch("choose_algorithm")
#    
#class GAParamsController:
#    def __init__(self, model: Model, view: View) -> None:
#        self.model = model
#        self.view = view
#        self.frame = self.view.frames["ga_params"]
#        self._bind()
#
#    def _bind(self) -> None:
#        """Binds controller functions with respective buttons in the view"""
#        self.frame.run_btn.config(command=self.choose_algorithm)
#
#    def choose_algorithm(self) -> None:
#        self.view.switch("choose_algorithm")