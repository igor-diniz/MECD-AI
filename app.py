from mvc.models.main import Model
from mvc.views.main import View
from mvc.controllers.main import Controller


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()

if __name__ == "__main__":
    main()