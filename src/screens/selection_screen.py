import sys
import pygame
from ui.card import Card
from screens.game_screen import GameScreen
from ui.colors import Colors
from ui.scrollbar import ScrollBar

class SelectionScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_text = self.font.render("Personajes disponibles", True, Colors.BLACK.value)

        self.__cards = []
        self.__characters = self.__load_characters()
        self.__selected_card_index = 0

        scrollbar = ScrollBar(self.screen_manager.window.get_height())

    def select_character(self):
        self.screen_manager.api.select_available_inhabitant(self.__cards[self.__selected_card_index].character['id'])

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.__cards[self.__selected_card_index].select()
                    self.select_character()
                    self.screen_manager.current_screen = GameScreen(self.screen_manager)
                elif event.key == pygame.K_w:
                    self.__selected_card_index -= 4
                elif event.key == pygame.K_s:
                    self.__selected_card_index += 4
                elif event.key == pygame.K_a:
                    self.__selected_card_index -= 1
                elif event.key == pygame.K_d:
                    self.__selected_card_index += 1
                
                # Ensure the selected index stays within bounds
                self.__selected_card_index = max(0, min(len(self.__cards)-1, self.__selected_card_index))

                # Deselect all cards and then select the current one
                for i, card in enumerate(self.__cards):
                    if i == self.__selected_card_index:
                        card.select()
                    else:
                        card.deselect()

    def update(self):
        pass

    def draw(self):
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.screen_manager.window.blit(self.title_text, (self.screen_manager.window.get_width() // 2 - self.title_text.get_width() // 2, 50))
        for card in self.__cards:
            card.draw()

    def __load_characters(self):
        self.screen_manager.api.get_available_inhabitants((10000, 10000), self.__update_cards)

    def __update_cards(self, characters_data):
        # card_width = self.screen_manager.window.get_width() // 2 - 50
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
