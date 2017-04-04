

class Class:
    features = []

    def __init__(self, features):
        self.features = features

    def hasFeature(self, index):
        return self.features[index] == 1

    def getBinaryData(self):
        return self.features