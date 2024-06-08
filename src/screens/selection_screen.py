import pygame
from screens.instructions_screen import InstructionsScreen
from ui.colors import Colors
from typing import List, Dict
from ui.card import CharacterCard
from ui.grid_layout import GridLayout
from screens.game_screen import GameScreen
from screens.screen import Screen

class SelectionScreen(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_text = self.font.render("Personajes disponibles", True, Colors.BLACK.value)
        self.characters = []
        self.grid_layout = GridLayout(screen_manager, 150, 100, 4, self.create_character_card, position=(85, 100), scroll_trigger=3)
        self.load_characters()
        self.selected_character = None

    def create_character_card(self, window, width, height, x, y, character):
        return CharacterCard(window, width, height, x, y, character)

    def load_characters(self):
        self.screen_manager.api.get_available_inhabitants((1000, 1000), self.update_cards)

    def update_cards(self, characters: List[Dict]):
        self.characters = characters
        self.grid_layout.update_cards(self.screen_manager.window, characters)

    def select_character(self):
        if self.grid_layout.cards:
            character_id = self.grid_layout.cards[self.grid_layout.selected_card_index].character['id']
            response = self.screen_manager.api.select_available_inhabitant(character_id)
            
            if response:
                character_info = self.screen_manager.api.get_inhabitant_information(character_id)
                father = self.screen_manager.api.get_inhabitant_information(character_info["father"])
                mother = self.screen_manager.api.get_inhabitant_information(character_info["mother"])

                character_info["family_tree"] = {
                    "id": character_info["id"],
                    "name": character_info["name"],
                    "father": {
                        "id": father["id"],
                        "name": father["name"],
                        "father": None,
                        "mother": None,
                        "children": [],
                        "siblings": []
                    },
                    "mother": {
                        "id": mother["id"],
                        "name": mother["name"],
                        "father": None,
                        "mother": None,
                        "children": [],
                        "siblings": []
                    },
                    "children": [],
                    "siblings": []
                }

                self.selected_character = character_info
                return True
            
            return False


    def handle_keydown(self, key: int):
        self.grid_layout.handle_keydown(key)
        if key == pygame.K_RETURN:
            self.grid_layout.cards[self.grid_layout.selected_card_index].select()
            if self.select_character():
                self.screen_manager.current_screen = GameScreen(self.screen_manager, self.selected_character)
                self.screen_manager.overlay_screen = InstructionsScreen(self.screen_manager)

    def update(self, *args, **kwargs):
        if "event" in kwargs:
            event = kwargs["event"]

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def draw(self):
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.screen_manager.window.blit(self.title_text, (self.screen_manager.window.get_width() // 2 - self.title_text.get_width() // 2, 50))
        self.grid_layout.draw(self.screen_manager.window)
