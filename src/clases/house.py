import pygame

class House:
    def __init__(self, house_info: dict, window: pygame.Surface, player_pos: tuple[int, int]):
        self.__id = int(house_info["id"])
        self.__window = window
        self.__x = int(house_info["x"]) - player_pos[0] + self.__window.get_width() // 2
        self.__y = int(house_info["y"]) - player_pos[1] + self.__window.get_height() // 2
        self.__occupants = house_info["occupants"]

        self.__image = pygame.image.load("src/assets/house_1.jpeg")
        self.__image = pygame.transform.scale(self.__image, (50, 50))
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = (self.__x, self.__y)
    
    def move(self, dx: int, dy: int):
        self.__x += dx
        self.__y += dy
        self.__rect.topleft = (self.__x, self.__y)

        self.draw()

    def draw(self):
        self.__window.blit(self.__image, self.__rect.topleft)

    # Properties

    @property
    def id(self):
        return self.__id

    
