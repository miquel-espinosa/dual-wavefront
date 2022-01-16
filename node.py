class Node(object):
    def __init__(self,xy,cost=0,parent=None,root=False) -> None:
        self.xy = xy
        self.root = root
        self.cost = cost
        self.parent = parent
        self.children = []

    
    def add_son(self,son):
        son.parent = self
        self.children.append(son)

    def find(self, xy):
        if self.xy == xy: return self
        for node in self.children:
            n = node.find(xy)
            if n: return n
        return None

    # def remove_son(self, xy):
    #     for child in self.children:
    #         if child.xy == xy:
    #             self.children.remove(child)
    #             break