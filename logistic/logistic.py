from numpy import *
# load data from file and write into list
def loadDataSet():
    dataMat = [];
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def stocGradAscent0(dataMatrix, classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):        dataIndex = range(m)
    for i in range(m):
        alpha = 4 / (1.0 + j + i) + 0.01
        randIndex = int(random.uniform(0, len(dataIndex)))
        h = sigmoid(sum(dataMatrix[randIndex] * weights))
        error = classLabels[randIndex] - h
        weights = weights + alpha * error * dataMatrix[randIndex]
        del (dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest(trainFile, testFile):
    frTrain = open(trainFile)
    frTest = open(testFile)
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
        trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 500)
        errorCount = 0;
        numTestVec = 0.0
        for line in frTest.readlines():
            numTestVec += 1.0
            currLine = line.strip().split('\t')
            lineArr = []
            for i in range(21):
                lineArr.append(float(currLine[i]))
            if int(classifyVector(array(lineArr), trainWeights)) !=\
                int(currLine[21]):
                errorCount += 1
        errorRate = (float(errorCount) / numTestVec)
        print("the error rate of this test is: %f" % errorRate)

        return errorRate

def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print("after %d iterations the average error rate is:\
    %f" % (numTests, errorSum/float(numTests)))
