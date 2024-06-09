from clases.game_data import GameDataManager


class CharacterNode:
    def __init__(self, character: dict):
        self.id = character["id"]
        self.name = character["name"]
        self.father = None
        self.mother = None
        self.children = []
        self.siblings = []

class FamilyTree:
    def __init__(self, player_data: dict):
        self.root = self._create_node(player_data)
        self._build_tree(player_data["family_tree"], self.root)

    def _create_node(self, character: dict) -> CharacterNode:
        return CharacterNode(character)

    def _build_tree(self, family_tree: dict, node: CharacterNode):
        if family_tree is None:
            return

        if "father" in family_tree and family_tree["father"] is not None:
            node.father = self._create_node(family_tree["father"])
            self._build_tree(family_tree["father"], node.father)

        if "mother" in family_tree and family_tree["mother"] is not None:
            node.mother = self._create_node(family_tree["mother"])
            self._build_tree(family_tree["mother"], node.mother)

        if "children" in family_tree:
            for child in family_tree["children"]:
                child_node = self._create_node(child)
                node.children.append(child_node)

        if "siblings" in family_tree:
            for sibling in family_tree["siblings"]:
                sibling_node = self._create_node(sibling)
                node.siblings.append(sibling_node)

    def to_dict(self) -> dict:
        """Convert the family tree to a dictionary."""
        def node_to_dict(node: CharacterNode) -> dict:
            return {
                "id": node.id,
                "name": node.name,
                "father": node_to_dict(node.father) if node.father else None,
                "mother": node_to_dict(node.mother) if node.mother else None,
                "children": [node_to_dict(child) for child in node.children],
                "siblings": [node_to_dict(sibling) for sibling in node.siblings]
            }

        return node_to_dict(self.root)

    @classmethod
    def from_dict(cls, data: dict):
        """Create a FamilyTree instance from a dictionary."""
        player_data = data.copy()
        player_data["family_tree"] = data
        return cls(player_data)

    def add_member(self, member: dict, relation: str, id: int, game_data: GameDataManager):
        node, level = self.get_node(id)
        member_node = CharacterNode(member)

        if relation == "father":
            node.father = member_node
        elif relation == "mother":
            node.mother = member_node
        elif relation == "sibling":
            node.siblings.append(member_node)
        elif relation == "child":
            node.children.append(member_node)

        # Update the game data with the new tree structure
        self._update_game_data(game_data)

    def _update_game_data(self, game_data: GameDataManager):
        """Update the game data with the current family tree structure."""
        game_data.data["family_tree"] = self.to_dict()
        game_data.data["family_tree"] = self.to_dict()
        game_data.save()

    def get_node(self, id: int) -> tuple[CharacterNode,  int]:
        return self._get_node(id, self.root, 0)

    def _get_node(self, id: int, node: CharacterNode, level: int) -> tuple[CharacterNode,  int]:
        if node.id == id:
            return node, level
        
        if node.father:
            father, lvl = self._get_node(id, node.father, level + 1)
            if father:
                return father, lvl
            
        if node.mother:
            mother, lvl = self._get_node(id, node.mother, level + 1)
            if mother:
                return mother, lvl
        
        for child in node.children:
            result, lvl = self._get_node(id, child, level + 1)
            if result:
                return result, lvl
            
        for sibling in node.siblings:
            result, lvl = self._get_node(id, sibling, level + 1)
            if result:
                return result, lvl

        return None, 0


        
