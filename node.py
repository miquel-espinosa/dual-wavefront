"""
    Class for tree Node
"""
class Node(object):
    def __init__(self,xy,cost=0,parent=None,root=False) -> None:
        self.xy = xy # Node coordinates
        self.root = root # Boolean: is this node tree root
        self.cost = cost # Cost of reaching this node from root
        self.parent = parent # Pointer to parent Node
        self.children = [] # Pointers to children Nodes

    def add_son(self,son):
        son.parent = self
        self.children.append(son)

    def find(self, xy):
        """ Find node in subtree """
        if self.xy == xy: return self
        for node in self.children:
            n = node.find(xy)
            if n: return n
        return None