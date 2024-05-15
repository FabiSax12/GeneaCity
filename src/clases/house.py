import pygame

class House:
    def __init__(self, house_info: dict, screen: pygame.Surface, player_pos: tuple[int, int]):
        self.id = int(house_info["id"])
        self.player_pos = player_pos
        self.screen = screen
        self.x = int(house_info["x"]) - self.player_pos[0] + self.screen.get_width() // 2
        self.y = int(house_info["y"]) - self.player_pos[1] + self.screen.get_height() // 2
        self.occupants = house_info["occupants"]

        self.image = pygame.image.load("src/assets/house_1.jpeg")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    
    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)


# position = (
#     self.screen.get_width() // 2 - player_pos[0],
#     self.screen.get_height() // 2 - player_pos[1]
# )

# self.x = self.screen.get_width() // 2 - player_pos[0]
# self.y = self.screen.get_height() // 2 - player_pos[1]

# print(self.x, self.y)

# if position[0] < -100:
#     position = (0, position[1])
# if position[1] > 0:
#     position = (position[0], 0)
# if position[0] < self.screen.get_width() - self.width:
#     position = (self.screen.get_width() - self.width, position[1])
# if position[1] < self.screen.get_height() - self.height:
#     position = (position[0], self.screen.get_height() - self.height)