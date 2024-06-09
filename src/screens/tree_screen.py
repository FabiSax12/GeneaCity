import math
import pygame
from screens.screen import Screen
from clases.tree import CharacterNode, FamilyTree
from ui.colors import Colors

class FamilyTreeScreen(Screen):
    """Family tree screen class."""
    
    def __init__(self, screen_manager, id: int):
        """Create a new instance of the FamilyTreeScreen class."""
        super().__init__(screen_manager)
        self.__font = pygame.font.Font(None, 15)
        self.__games = self.screen_manager.game_data.load()
        self.__family_tree = FamilyTree(list(filter(lambda x: x["id"] == id, self.__games))[0])
        self.__offset_x = 200
        self.__offset_y = -500
        self.__node_height = 130
        self.__node_radius = 30
        self.__node_distance = 200

    def draw(self):
        """Draw the family tree."""
        self.screen_manager.window.fill(Colors.WHITE.value)
        self.draw_tree(self.__family_tree.root, 0, self.screen_manager.window.get_width() * 1.5 , 100)
    
    def update(self, *args, **kwargs):
        """Update the family tree screen."""
        if "event" in kwargs:
            event = kwargs["event"]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.__offset_y -= 20
                elif event.key == pygame.K_s:
                    self.__offset_y += 20
                elif event.key == pygame.K_a:
                    self.__offset_x -= 20
                elif event.key == pygame.K_d:
                    self.__offset_x += 20

                if event.key == pygame.K_ESCAPE:
                    del self.screen_manager.overlay_screen
    
    def draw_tree(self, character, xmin, xmax, y):
        """Draw the family tree."""
        if not isinstance(character, CharacterNode):
            print(character)
            
        x = xmin + (xmax - xmin) // 2
        pygame.draw.circle(self.screen_manager.window, Colors.DARK_GREEN.value, (x - self.__offset_x, y - self.__offset_y), self.__node_radius)
        text = self.__font.render(character.name.split(" ")[0], True, Colors.WHITE.value)
        self.screen_manager.window.blit(text, (x - text.get_width() / 2 - self.__offset_x, y- text.get_height() / 2 - self.__offset_y))
        
        father_x = xmin + (x - xmin) // 2
        mother_x = x + (xmax - x) // 2

        # if mother_x - father_x < 200:
        #     father_x -= 100
        #     mother_x += 100

        if character.father:
            inicial_point = (x - self.__offset_x, y - self.__offset_y)
            final_point = (father_x - self.__offset_x, y - self.__node_height - self.__offset_y)

            pygame.draw.line(
                self.screen_manager.window,
                Colors.BROWN.value, 
                self.calculate_circle_border(
                    inicial_point[0], inicial_point[1], 
                    final_point[0], final_point[1], 
                    self.__node_radius
                ),
                final_point,
                2
            )
            self.draw_tree(character.father, xmin, x, y - self.__node_height)
        
        if character.mother:
            
            inicial_point = (x - self.__offset_x, y - self.__offset_y)
            final_point = (mother_x - self.__offset_x, y - self.__node_height - self.__offset_y)

            pygame.draw.line(
                self.screen_manager.window,
                Colors.BROWN.value, 
                self.calculate_circle_border(
                    inicial_point[0], inicial_point[1], 
                    final_point[0], final_point[1], 
                    self.__node_radius
                ),
                final_point,
                2
            )

            self.draw_tree(character.mother, x, xmax, y - self.__node_height)

        child_y = y + self.__node_height
        child_spacing = (xmax - xmin) // (len(character.children) + 1)
        for i, child in enumerate(character.children):
            child_x = xmin + (i + 1) * child_spacing
            inicial_point = (x - self.__offset_x, y - self.__offset_y)
            final_point = (child_x - self.__offset_x, child_y - self.__offset_y)

            pygame.draw.line(
                self.screen_manager.window,
                Colors.BROWN.value, 
                self.calculate_circle_border(
                    inicial_point[0], inicial_point[1], 
                    final_point[0], final_point[1], 
                    self.__node_radius
                ),
                final_point,
                2
            )

            self.draw_tree(child, child_x - child_spacing // 2, child_x + child_spacing // 2, child_y)

        # Draw siblings
        sibling_y = y
        sibling_spacing = 60 # (xmax - xmin) // (len(character.siblings) + 1)
        inicial_x = x - self.__node_radius * 2

        for i, sibling in enumerate(character.siblings):
            # sibling_x = inicial_x + (xmin + (i) * sibling_spacing)
            # sibling_x *= -1 if i % 2 == 0 else 1
            # sibling_x += inicial_x + 400 - self.__node_radius * 2 if i % 2 == 0 else 0
            sibling_x = x + ((i + 1) * sibling_spacing) * ( -1 if i % 2 == 0 else 1 ) - self.__node_radius

            self.draw_tree(sibling, sibling_x, sibling_x, sibling_y)

    def calculate_circle_border(self, x_c, y_c, x_f, y_f, r):
        # Calculate the angle between the center of the circle and the point
        theta = math.atan2(y_f - y_c, x_f - x_c)
        
        # Calculate the point on the circle
        x_b = x_c + r * math.cos(theta)
        y_b = y_c + r * math.sin(theta)
        
        return (x_b, y_b)
