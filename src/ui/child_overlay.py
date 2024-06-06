from screens.screen import Screen
from ui.input import Input, NumberInput
from ui.button import Button

class ChildOverlay(Screen):
    def __init__(self, screen_manager, child_callback):
        super().__init__(screen_manager)
        self.__create_child = child_callback

        self.__title = self.screen_manager.text_renderer.render_text(
            "Defina las características de su hijo", 
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
            Input(
                "Nombre",
                (self.screen_manager.window.get_width() // 2 - 110, self.screen_manager.window.get_height() // 2 - 100),
                size=(200, 25),
                font_size=16,
                border_radius=1,
            ),
            Input(
                "Género",
                (self.screen_manager.window.get_width() // 2 - 110, self.screen_manager.window.get_height() // 2 - 50),
                size=(200, 25),
                font_size=16,
                border_radius=1
            ),
            NumberInput(
                "Edad",
                (self.screen_manager.window.get_width() // 2 - 110, self.screen_manager.window.get_height() // 2),
                min=0,
                max=100,
                size=(200, 25),
                font_size=16,
                border_radius=1
            )
        ]

        self.__agree_button = Button(
            "Crear hijo",
            (self.screen_manager.window.get_width() // 2 - 100, self.screen_manager.window.get_height() // 2 + 50),
            lambda: self.__create_child(
                self.__inputs[0].get_text(), 
                self.__inputs[1].get_text(),
                self.__inputs[2].get_text()
            ),
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
            size=(200, 25)
        )

        self.__close_button = Button(
            "Cerrar",
            (self.screen_manager.window.get_width() // 2 - 100, self.screen_manager.window.get_height() // 2 + 100),
            self.screen_manager.delete_overlay,
            bg_color=(0, 122, 204),
            text_color=(255, 255, 255),
            hover_bg_color=(0, 162, 255),
            size=(200, 25)
        )

    def update(self, *args, **kwargs):
        if "event" in kwargs:
            event = kwargs["event"]
            for input in self.__inputs:
                input.handle_event(event)
            self.__agree_button.handle_event(event)
            self.__close_button.handle_event(event)
    
    def draw(self):
        self.screen_manager.window.blit(self.__title[0], self.__title[1])
        for input in self.__inputs:
            input.draw(self.screen_manager.window)
        self.__agree_button.draw(self.screen_manager.window)
        self.__close_button.draw(self.screen_manager.window)
