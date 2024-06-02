import time
import pygame


class Toast:
    def __init__(self, message, x, y, w, h, duration=2, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
        self.message = message
        self.__text_color = text_color
        self.__bg_color = bg_color
        self.font = pygame.font.Font(None, 14)
        self.txt_surface = self.font.render(message, True, text_color)
        self.rect = pygame.Rect(800 - self.txt_surface.get_width() - 20, y, self.txt_surface.get_width() + 20, h)
        self.alpha = 0
        self.duration = duration
        self.start_time = time.time()
        self.fade_in = True
        self.visible = False

    def update(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if self.fade_in:
            self.alpha += 5
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
                self.visible = True
                self.start_time = current_time
        elif self.visible and elapsed_time >= self.duration:
            self.visible = False
            self.start_time = current_time
        elif not self.visible:
            self.alpha -= 5
            if self.alpha <= 0:
                self.alpha = 0
                self.visible = False

    def draw(self, screen):
        if not self.visible:
            return
        surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        surface.fill((*self.__bg_color, self.alpha))
        text_surface = self.font.render(self.message, True, self.__text_color)
        surface.blit(text_surface, (5, 5))
        screen.blit(surface, (self.rect.x, self.rect.y))