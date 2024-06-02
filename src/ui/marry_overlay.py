from ui.button import Button
from screens.screen import Screen
from ui.input import NumberInput

class MarryOverlay(Screen):
    def __init__(self, screen_manager, couple, marry_callback):
        super().__init__(screen_manager)
        self.__marry = marry_callback
        self.__couple_name = couple["name"]

        self.__title = self.screen_manager.text_renderer.render_text(
            f"Escoja las coordenadas para vivir con {self.__couple_name}", 
            "default", 
            (
                "center", 
                (
                    self.screen_manager.window.get_width() // 2,
                    self.screen_manager.window.get_height() // 2 - 150
                )
            )
        )

        self.__inputs = [
            NumberInput(
                "Coordenada X",
                (self.screen_manager.window.get_width() // 2 - 110, self.screen_manager.window.get_height() // 2 - 100),
                min=0,
                max=100000,
                size=(100, 25),
                font_size=16,
                border_radius=1,
            ),
            NumberInput(
                "Coordenada Y",
                (self.screen_manager.window.get_width() // 2 + 10, self.screen_manager.window.get_height() // 2 - 100),
                min=0,
                max=100000,
                size=(100, 25),
                font_size=16,
                border_radius=1
            )
        ]

        self.__marry_button = Button(
            "Aceptar",
            (self.screen_manager.window.get_width() // 2 - 100, self.screen_manager.window.get_height() // 2 - 25),
            lambda: self.__marry(couple["id"], self.__inputs[0].get_text(), self.__inputs[1].get_text(), self.__handle_marry_error)
        )

    def update(self, *args, **kwargs):
        if "event" in kwargs:
            event = kwargs["event"]
            for input in self.__inputs:
                input.handle_event(event)
            self.__marry_button.handle_event(event)
    
    def draw(self):
        self.screen_manager.window.blit(self.__title[0], self.__title[1])
        for input in self.__inputs:
            input.draw(self.screen_manager.window)
        self.__marry_button.draw(self.screen_manager.window)

    def __handle_marry_error(self, error: ValueError):
        if "There is already a house very close to this location." == error.args[0]:
            self.screen_manager.show_toast(error.args[0], 3)

        print("Error:", error)