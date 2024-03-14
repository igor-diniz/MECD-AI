from typing import TypedDict
from .home import HomeView
from .root import Root
from .algorithm.choose import ChooseAlgorithmView
from .algorithm.params import AlgorithmParamsView, HCParamsView, SAParamsView, TSParamsView, GAParamsView
from .algorithm.results import AlgorithmResultsView

class Frames(TypedDict):
    home: HomeView
    choose_algorithm: ChooseAlgorithmView
    params: AlgorithmParamsView
    hc_params: HCParamsView
    sa_params: SAParamsView
    ts_params: TSParamsView
    ga_params: GAParamsView

class View:
    def __init__(self):
        self.root = Root()
        self.frames: Frames = {}
        self._add_frame(ChooseAlgorithmView, "choose_algorithm")
        self._add_frame(AlgorithmParamsView, "params")
        self._add_frame(HCParamsView, "hc_params")
        self._add_frame(SAParamsView, "sa_params")
        self._add_frame(TSParamsView, "ts_params")
        self._add_frame(GAParamsView, "ga_params")
        self._add_frame(AlgorithmResultsView, "alg_results")
        self._add_frame(HomeView, "home")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self) -> None:
        self.root.mainloop()