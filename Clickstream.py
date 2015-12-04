__author__ = 'gp'

import csv
import math
import sys;
import time;

from DTreeNode import DTreeNode;
from PageView import PageView;
from Chi import Chi;
from itertools import izip;

FEATURES  = 274;
nodeCount = 0;
sys.setrecursionlimit(1500000);

class Clickstream:

    @staticmethod
    def main():
       global FEATURES,nodeCount;
       thresh = 1;
       #thresh = input('Enter Threshold Value::');
       #Array of string feature names
       featNames = [];
       trainFeat = set();
       testFeat  = set();

       with open('DataSet/featnames.csv', 'rb') as f:
        reader = csv.reader(f);
        for row in reader:
            featNames.append(row[0]);

       Clickstream.buildDataMaps(trainFeat, "./DataSet/trainfeat.csv", "./DataSet/trainlabs.csv");
       Clickstream.buildDataMaps(testFeat,  "./DataSet/testfeat.csv",  "./DataSet/testlabs.csv");

       j=0;
       while(j < FEATURES):
            Clickstream.computeRange(trainFeat, j);
            j = j + 1;
       sys.exit();

       #most important call
       root = Clickstream.learnTree(trainFeat, featNames, set(), thresh);

       #Writing results to external file
       labels = [];
       f = open("clickstream_results.txt","w");
       for pageView in testFeat:
            label = int(Clickstream.predictTree(pageView, root));
            labels.append(label);
            f.write(str(label));
            f.write("\n");
       f.close();

       print "Test-Data Prediciton Statistics"
       print "-------------------------------"
       print "Tree Size::",nodeCount;
       Clickstream.computeAccuracy(testFeat, labels);

    @staticmethod
    #buildDataMaps(trainFeat, "./DataSet/trainfeat.csv", "./DataSet/trainlabs.csv");
    def buildDataMaps(pageViews, featurePath, labPath):
        with open(featurePath) as data, open(labPath) as labs:
            for x, y in izip(data, labs):
                label = int(y.strip());#labs
                dataLine = x.strip();#dataLine

                sc = dataLine;#dataLine
                features = [];

                for ind_temp in sc:
                    if(not(ind_temp ==" " or ind_temp==' ')):
                        features.append(int(ind_temp));
                pageViews.add(PageView(int(label), features));

            print "len(pageViews)::",len(pageViews);
            time.sleep(1);
        data.close();
        labs.close();

    @staticmethod
    #root = ClickStream.learnTree(trainFeat, featNames, set(), thresh);
    def learnTree(pageViews, featNames, testAttr, thresh):

        global nodeCount;
        #print "nodeCount::",nodeCount;
        nodeCount = nodeCount + 1;
        positive = 0;

        for pageView in pageViews:
            #print "pageView.getLabel()::",pageView.getLabel();
            if(int(pageView.getLabel()) == 1):
                positive = positive + 1;

        #sys.exit();

        if (positive == len(pageViews)):
            return DTreeNode(None, 0, 0, None, 1);
        else:
            if(positive == 0):
                return DTreeNode(None, 0, 0, None, 0);
            else:
                if(len(testAttr) == FEATURES):
                    if(positive >= (len(pageViews) - positive)):
                        return DTreeNode(None, 0, 0, None, 1);
                    else:
                        return DTreeNode(None, 0, 0, None, 0);
                else:
                    attrIndex = -1;
                    maxGain = -float('inf');
                    i = 0;
                    while(i < FEATURES):
                        if(not(i in testAttr)):
                            #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
                            gain = float(Clickstream.informationGain(pageViews, i));
                            #print "gain::",gain;

                            print "maxGain < gain::",maxGain,gain;
                            time.sleep(1);

                            if( maxGain < gain ):
                                maxGain = gain;
                                attrIndex = i;
                            #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
                        i = i + 1;

                    range = Clickstream.computeRange(pageViews , attrIndex);
                    #print "range.size()",len(range);
                    chi_obj = Chi();

                    arg1 = float(Clickstream.chiSquare(positive, len(pageViews), range));
                    arg2 = float(chi_obj.critchi(float(thresh) , len(range) - 1));

                    if( arg1 <= arg2 ):
                        if(positive >= (len(pageViews) - positive)):
                            return DTreeNode(None, 0, 0, None, 1);
                        else:
                            return DTreeNode(None, 0, 0, None, 0);
                    if((positive >= (len(pageViews) - positive))):
                        defaultLabel = 1;
                    else:
                        defaultLabel = 0;
                    #Same as hashmap
                    node = DTreeNode(featNames[attrIndex], attrIndex, defaultLabel, {}, 0);
                    testAttr.add(attrIndex);

                    for value in range:
                        node.getBranches().update({value : Clickstream.learnTree(range[value], featNames, set() , thresh)});
                    return node;

    @staticmethod
    def computeRange(pageViews, attributeIndex):
       values = {};
       for pageView in pageViews:
           value = int(pageView.getFeatures()[attributeIndex]);

           if(not(value in values)):
               values.update({value : set()});
           values[value].add(pageView);

       print "len(values)::",len(values);
       time.sleep(1);
       return values;

    @staticmethod
    def informationGain(pageViews, attributeIndex):
        entropyS  = float(Clickstream.entropy(pageViews));
        gain      = float(0);
        values    = Clickstream.computeRange(pageViews, attributeIndex);

        for value in values:
            gain_arg1 = len(values[value]);
            gain_arg2 = float((len(pageViews)));
            gain_arg3 = Clickstream.entropy(values[value]);
            gain = gain + (gain_arg1 / gain_arg2) * gain_arg3;

        return float(entropyS - gain);

    @staticmethod
    def computeAccuracy(pageViews, labels):
        correct  = 0;
        index    = 0;
        for pageView in pageViews:
            if(str(pageView.getLabel()) == str(labels[index])):
                correct = correct + 1;
            index = index + 1;

        print "Matches::", correct;
        print "Accuracy of Prediction::", round((100.0 * correct)/len(labels),2);

    @staticmethod
    def chiSquare(positive, total, range):
        sum = float(0);
        for value in range:
            pPrime  = float(positive) * len(range[value]) / total;
            nPrime  = float((total - positive)) * len(range[value]) / total;
            pos = int(0);
            for pageView in range[value]:
                if (int(pageView.getLabel()) == 1):
                    pos = pos + 1;
            sum = float(sum) + float((math.pow(pPrime - pos, 2) / pPrime)) + \
                  float((math.pow((nPrime - (len(range[value])) - pos), 2) / nPrime));
        return sum;

    @staticmethod
    def entropy(pageViews):
        tot = len(pageViews);
        pos= 0;
        for p in pageViews:
            if(int(p.getLabel()) == 1):
                pos = pos + 1;
        if (pos == 0 or pos == tot):
            return 0;
        pProp = float((-1.0 * pos / tot) * math.log(1.0 * pos / tot) / math.log(2));
        nProp = float((1.0 * (tot - pos) / tot) * math.log(1.0 * (tot - pos) / tot) / math.log(2));
        return float(pProp - nProp);

    @staticmethod
    def predictTree(pageView, root):
        if(root.getBranches() == None):
            return root.getLabel();
        value = pageView.getFeatures()[root.getIndex()];
        if(root.getBranches[value] == None):
            return root.getDefaultLabel();
        return Clickstream.predictTree(pageView , root.getBranches()[value]);

#Calling Application
Clickstream.main();