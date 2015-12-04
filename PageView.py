__author__ = 'gp'

class PageView:

    def __init__(self,label,features):
        self.label   = label;
        self.features = features;

    def getLabel(self):
        return int(self.label);

    def getFeatures(self):
        return self.features;
