class Tree:
    def __init__(self, root):
        self.root = root
        self.children = []

    def set_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f"Arbol: {self.root}"

class BinaryTree(Tree):
    def __init__(self, name, left=None, right=None):
        super().__init__(name)
        self.left = left
        self.right = right

    def set_child(self, child, side):
        if side == "izquierda":
            self.left = child
        elif side == "derecha":
            self.right = child

    def __str__(self):
        return f"Arbol Binario: {self.root}"

class GenealogicTree(Tree):
    def __init__(self, name, children=None):
        super().__init__(name)
        self.children = children

    def set_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f"Arbol Genealogico: {self.root}"
    
