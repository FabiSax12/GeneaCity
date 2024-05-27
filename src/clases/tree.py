import sys
import pygame


# Datos de ejemplo
player_data = {
    "name": "Player",
    "father": "Father",
    "mother": "Mother"
}

family_data = []

class CharacterNode:
    def __init__(self, name: str):
        self.name = name
        self.father = None
        self.mother = None

    def __repr__(self):
        return f"CharacterNode({self.name})"

class FamilyTree:
    def __init__(self):
        self.nodes = {}

    def add_character(self, name: str, father_name: str = None, mother_name: str = None):
        """Add a character and their parents to the tree."""
        if name not in self.nodes:
            self.nodes[name] = CharacterNode(name)
        
        if father_name:
            if father_name not in self.nodes:
                self.nodes[father_name] = CharacterNode(father_name)
            self.nodes[name].father = self.nodes[father_name]

        if mother_name:
            if mother_name not in self.nodes:
                self.nodes[mother_name] = CharacterNode(mother_name)
            self.nodes[name].mother = self.nodes[mother_name]

    def get_character(self, name: str) -> CharacterNode:
        """Get a character node by name."""
        return self.nodes.get(name)

    def display_tree(self, name: str, level: int = 0):
        """Display the family tree starting from the given character."""
        character = self.get_character(name)
        if character:
            if character.father:
                self.display_tree(character.father.name, level + 1)
            if character.mother:
                self.display_tree(character.mother.name, level + 1)

class FamilyTreeUI:
    def __init__(self, family_tree, character_name, screen):
        self.family_tree = family_tree
        self.character_name = character_name
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.node_height = 80
        self.node_radius = 30

    def draw_tree(self, character_name, xmin, xmax, y):
        character = self.family_tree.get_character(character_name)
        if character:
            x = xmin + (xmax - xmin) // 2

            if character.father:
                father_x = xmin + (x - xmin) // 2
                pygame.draw.line(self.screen, pygame.Color("darkgreen"), (x, y), (father_x, y - self.node_height), 2)
                self.draw_tree(character.father.name, xmin, x, y - self.node_height)

            if character.mother:
                mother_x = x + (xmax - x) // 2
                pygame.draw.line(self.screen, pygame.Color("darkgreen"), (x, y), (mother_x, y - self.node_height), 2)
                self.draw_tree(character.mother.name, x, xmax, y - self.node_height)

            pygame.draw.circle(self.screen, pygame.Color("darkgreen"), (x, y), self.node_radius)
            pygame.draw.circle(self.screen, pygame.Color("darkgreen"), (x, y), self.node_radius, 2)
            text_surface = self.font.render(character.name, True, pygame.Color("white"))
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(pygame.Color("darkgray"))
        self.draw_tree(self.character_name, 0, self.screen.get_width(), self.screen.get_height() - self.node_height)
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Family Tree")

    # Crear el árbol genealógico
    family_tree = FamilyTree()
    family_tree.add_character(player_data["name"], player_data["father"], player_data["mother"])

    for data in family_data:
        family_tree.add_character(data["name"], data.get("father"), data.get("mother"))

    tree_ui = FamilyTreeUI(family_tree, "Player", screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tree_ui.draw()

if __name__ == "__main__":
    main()
