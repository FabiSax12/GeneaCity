import sys
import pygame
from typing import Literal
from ui.card import Card
from ui.colors import Colors
from screens.game_screen import GameScreen

class SelectionScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_text = self.font.render("Personajes disponibles", True, Colors.BLACK.value)

        self.__cards = []
        self.__characters = self.__load_characters()
        self.__selected_card_index = 0

        self.__cards_scroll = 0

    def select_character(self):
        self.screen_manager.api.select_available_inhabitant(self.__cards[self.selected_card_index].character['id'])

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.__cards[self.selected_card_index].select()
                    self.select_character()
                    self.screen_manager.current_screen = GameScreen(self.screen_manager)
                elif event.key == pygame.K_w:
                    if self.selected_card_index >= 4:
                        self.selected_card_index -= 4
                        if self.selected_card_index // 4 < self.__cards_scroll:
                            self.scroll("up")

                elif event.key == pygame.K_s:
                    if self.selected_card_index + 4 < len(self.__cards):
                        self.selected_card_index += 4
                        if self.selected_card_index // 4 > self.__cards_scroll + 3:
                            self.scroll("down")

                elif event.key == pygame.K_a:
                    if self.selected_card_index % 4 > 0:
                        self.selected_card_index -= 1
                elif event.key == pygame.K_d:
                    if (self.selected_card_index + 1) % 4 != 0 and self.selected_card_index + 1 < len(self.__cards):
                        self.selected_card_index += 1

                for i, card in enumerate(self.__cards):
                    if i == self.selected_card_index:
                        card.select()
                    else:
                        card.deselect()

    def update(self):
        pass

    def draw(self):
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.screen_manager.window.blit(self.title_text, (self.screen_manager.window.get_width() // 2 - self.title_text.get_width() // 2, 50))
        start_index = self.__cards_scroll * 4
        end_index = start_index + 4 * 6
        for card in self.__cards[start_index:end_index]:
            card.draw()

    def scroll(self, direction: Literal["up", "down"]):
        if direction == "down" and self.__cards_scroll < (len(self.__cards) - 1) // 4:
            self.__cards_scroll += 1
        elif direction == "up" and self.__cards_scroll > 0:
            self.__cards_scroll -= 1

        dy = 110 if direction == "down" else -110
        for card in self.__cards:
            card.position = (card.position[0], card.position[1] - dy)

    def __load_characters(self):
        self.screen_manager.api.get_available_inhabitants((10000, 10000), self.__update_cards)

    def __update_cards(self, characters_data):
        card_width = 150
        card_height = 100

        self.__cards = [
            Card(
                self.screen_manager.window,
                card_width,
                card_height,
                85 + card_width * (i % 4) + 10 * (i % 4),
                100 + card_height * (i // 4) + 10 * (i // 4),
                character
            ) for i, character in enumerate(characters_data)
        ]

        self.__cards[0].select()

    @property
    def selected_card_index(self):
        return self.__selected_card_index
    
    @selected_card_index.setter
    def selected_card_index(self, value: int):
        self.__selected_card_index = max(0, min(len(self.__cards) - 1, value))