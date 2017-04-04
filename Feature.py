

class Feature:

    childrenNodes = None
    chance = 0
    id = 0


    def __init__(self, id):
        self.childrenNodes = []
        self.id = id

    def addChild(self, child):
        self.childrenNodes.append(child)

    def setChance(self, p):
        self.chance = p

    def __str__(self):
        return str(id)