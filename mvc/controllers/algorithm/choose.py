from mvc.views.main import View
from mvc.models.main import Model

class ChooseAlgorithmController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["choose_algorithm"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.hc_btn.config(command=self.choose_hc)
        self.frame.sa_btn.config(command=self.choose_sa)
        self.frame.ts_btn.config(command=self.choose_ts)
        self.frame.ga_btn.config(command=self.choose_ga)

    def choose_hc(self) -> None:
        self.view.switch("hc_params")

    def choose_sa(self) -> None:
        self.view.switch("sa_params")
    
    def choose_ts(self) -> None:
        self.view.switch("ts_params")
    
    def choose_ga(self) -> None:
        self.view.switch("ga_params")
