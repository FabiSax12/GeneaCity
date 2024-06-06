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

    def get_node(self, id: int) -> CharacterNode:
        return self._get_node(id, self.root)

    def _get_node(self, id: int, node: CharacterNode) -> CharacterNode:
        if node.id == id:
            return node
        
        for child in node.children:
            result = self._get_node(id, child)
            if result:
                return result

        return None

    def get_siblings(self, id: int) -> list:
        node = self.get_node(id)
        return node.siblings
    
    def get_parents(self, id: int) -> tuple:
        node = self.get_node(id)
        return node.father, node.mother
    
    def get_children(self, id: int) -> list:
        node = self.get_node(id)
        return node.children
    
    def add_member(self, member: dict, relation: str, id: int):
        node = self.get_node(id)
        member_node = CharacterNode(member)

        if relation == "father":
            node.father = member_node
        elif relation == "mother":
            node.mother = member_node
        elif relation == "sibling":
            node.siblings.append(member_node)
        elif relation == "child":
            node.children.append(member_node)

    def save(self):
        return self._save(self.root)
    
    def _save(self, node: CharacterNode) -> dict:
        data = self.scre
        data = {
            "id": node.id,
            "name": node.name
        }

        if node.father is not None:
            data["father"] = self._save(node.father)
        
        if node.mother is not None:
            data["mother"] = self._save(node.mother)
        
        if node.children:
            data["children"] = [self._save(child) for child in node.children]

        return data


        
