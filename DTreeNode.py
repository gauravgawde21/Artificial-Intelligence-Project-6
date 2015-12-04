__author__ = 'gp'

class DTreeNode:
    def __init__(self, attributeName, attributeIndex, defaultLabel , branches , label):
        self.attributeName  = attributeName;
        self.attributeIndex = attributeIndex;
        self.defaultLabel   = defaultLabel;
        self.branches       = branches;
        self.label          = label;

    def getName(self):
        self.attributeName;

    def getIndex(self):
        self.attributeIndex;

    def getLabel(self):
        return self.label;

    def getDefaultLabel(self):
        return self.defaultLabel;

    def getBranches(self):
        return self.branches;
