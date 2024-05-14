import pygame
from characters.player  import Player
from clases.house   import House

player_mock = {
    "id": 1, 
    "name": "John", 
    "age": 25, 
    "house": {"x": 250, "y": 250}
}

class EventHandler:
    def __init__(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

class Renderer:
    def __init__(self, screen: pygame.Surface, houses: list[House]):
        self.screen = screen
        self.houses = houses
    
    def update_houses(self, houses_info: list[dict]):
        house_ids = [house_info["id"] for house_info in houses_info]
        for house in self.houses:
            if house.id not in house_ids:
                self.houses.remove(house)
        
        for house_info in houses_info:
            if house_info["id"] not in [house.id for house in self.houses]:
                self.houses.append(House(house_info))

    def render(self, player: Player):
        # self.screen.fill(Colors.GRASS.value)
        for house in self.houses:
            house.draw(self.screen)
        player.draw(self.screen)
        pygame.display.flip()


class InputHandler:
    def __init__(self, player: Player):
        self.player = player

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.player.move(0, -300 * dt)
        if keys[pygame.K_s]: self.player.move(0, 300 * dt)
        if keys[pygame.K_a]: self.player.move(-300 * dt, 0)
        if keys[pygame.K_d]: self.player.move(300 * dt, 0)
        if keys[pygame.K_ESCAPE]: pygame.quit()