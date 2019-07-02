from math import *
import operator


# calculate Shannon Entropy for any dataset containing data vector lists
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


# split the raw dataset according to whatever feature it have
def splitDataSet(dataSet, featureIndex, featureValue):
    retDataSet = []
    for featVec in dataSet:
        if featVec[featureIndex] == featureValue:
            reducedFeatVec = featVec[:featureIndex]
            reducedFeatVec.extend(featVec[featureIndex + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


# use ID3 decision tree
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# create a decision tree for any Dataset with any amount of features and discrete feature values
def createTree(DataSet, labels):
    classList = [example[-1] for example in DataSet]
    # if there is only one class
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # if the class of final branch is not unique
    if len(DataSet[0]) == 1:
        # vote for a unique class the data should belong to
        return majorityCnt(classList)
    # if there is not only one class and is not final branch
    # get the best split feature index
    bestFeat = chooseBestFeatureToSplit(DataSet)
    # get the best split feature name
    bestFeatLabel = labels[bestFeat]

    # every tree is depicted as a dictionary
    myTree = {bestFeatLabel: {}}

    # delete the best split feature so as to recurse the method
    del(labels[bestFeat])

    # get the set of best split feature value
    featValues = [example[bestFeat] for example in DataSet]
    featValuesSet = set(featValues)

    # for each feature value, try to get child-tree of the value of node (feature)
    for featValue in featValuesSet:
        # subLabel is a label list without the parent feature
        subLabels = labels
        # construct a child tree for each feature value of parent feature
        myTree[bestFeatLabel][featValue] = createTree(splitDataSet\
                                        (DataSet, bestFeat, featValue), subLabels)

    return myTree


# test a data vector using decision tree
def classify(inputTree, featLabels, testVec):
    # in any tree, there is only one root node
    parentNode = inputTree.keys()[0]
    parentBranch = inputTree[parentNode]
    parentFeatIndex = featLabels.index(parentNode)
    classLabel = None
    for branch in parentBranch.keys():
        # for any feature in testVec, their value must be in decision tree branch
        if testVec[parentFeatIndex] == branch:
            # judge if the node in this branch is leaf node
            if type(parentBranch[branch]).__name__ == 'dict':
                classLabel = classify(parentBranch[branch], featLabels, testVec)
            else: classLabel = parentBranch[branch]
    return classLabel





def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]


    labels = ['no surfacing', 'flippers']
    return dataSet, labels

