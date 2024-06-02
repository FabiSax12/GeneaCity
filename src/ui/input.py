import pygame

class Input:
    def __init__(self, label, position, size=(200, 50), font_size=24, bg_color=(100, 100, 100), text_color=(255, 255, 255), border_radius=10):
        self.label = label
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        
        self.font = pygame.font.Font(None, font_size)
        self.rect = pygame.Rect(position, size)
        self.text_surface = self.font.render(label, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.text_surface, (self.position[0], self.position[1] - 15))
        screen.blit(self.font.render(self.text, True, self.text_color), (self.position[0] + 10, self.position[1] + 10))
        if self.active:
            pygame.draw.rect(screen, self.text_color, self.rect, 2, border_radius=self.border_radius)
        else:
            pygame.draw.rect(screen, self.text_color, self.rect, 2, border_radius=self.border_radius)

    def get_text(self):
        return self.text
    
class NumberInput(Input):
    def __init__(self, label, position, min=0, max=0, size=(200, 50), font_size=24, bg_color=(100, 100, 100), text_color=(255, 255, 255), border_radius=10):
        super().__init__(label, position, size=size, font_size=font_size, bg_color=bg_color, text_color=text_color, border_radius=border_radius)
        self.min = min
        self.max = max

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

    def get_text(self):
        try:
            return int(self.text)
        except ValueError:
            return 0
        
    
            