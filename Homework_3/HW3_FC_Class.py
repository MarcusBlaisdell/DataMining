########################
### Marcus Blaisdell
### Cpt_S 315
### Homework #3
###
### HW3_FC_Class.py
###
########################

########################
### 1. initialize the weights, w = 0
### 2. for each training iteration, do:
### 3.    for each training example, do:
### 4.       yHat = sign(w*xt) // predict using current weights
### 5.       if mistake, then
### 6.          w = w + eta * yt * xt // update the weights
### 7.       end if
### 8.    end for
### 9. end for
### 10. return final weight vector w
###
########################

import numpy as np
from HW3_Functions import sign

class FCookie():
    ### attributes:
        # dictionary let's us utilize the hash functions for faster searching
    stopList = {}
        # lists to utilize indexing:
    trainData = []
    trainLabel = []
    testData = []
    testLabel = []
    vocabulary = []
    featureVectorList = []
    testVectorList = []
    eta = 1 # learning ratingIndex
    w = np.array([0]) # weight vector
    wCache = np.array([0]) # cached weight vector
    m = 0
    maxIteration = 20
    numberOfMistakes = []
    standardTrainingAccuracy = []
    standardTestingAccuracy = []
    averagedTrainingAccuracy = []
    averagedTestingAccuracy = []

        ### initialize the class:
    def __init__(self):
        pass
    ### end __init__

    ### readStops function
    ### read the words from the stoplist text fileName
    ### into a dictionary
    ### the dictionary makes it faster to search
    ### whether or not a word is in the stoplist or not

    def readStops(self, fileName):
        inFile = open (fileName, "r")

        string = ''
        word = ''

        string = inFile.readline()

        while string:
            for letter in range(len(string)):
                if letter == len(string) - 1:
                    if string[letter] != '\r' and string[letter] != '\n':
                        word += string[letter]
                    ### if the word is not in the dictionary, add it, else,
                    ### no action required
                    if self.stopList.get(word, 'n') == 'n':
                        self.stopList[word] = 1
                    word = ''
                elif letter == ' ':
                    self.stopList.append(word)
                    word = ''
                else:
                    word += string[letter]

            string = inFile.readline()

        inFile.close()
    ### end readStops

    ### read the fortunes into a list for processing:

    def readLines(self, fileName, dataName):
        inFile = open (fileName, "r")

        lineList = []
        word = ''

        string = inFile.readline()

        while string:

            for letter in range(len(string)):
                if letter == len(string) - 1:
                    lineList.append(word)
                    dataName.append (lineList)
                    lineList = []
                    word = ''
                elif string[letter] == ' ':
                    lineList.append(word)
                    word = ''
                else:
                    word += string[letter]

            string = inFile.readline()

        inFile.close()

    ### end readLines

    ### read the labels into a list for processing
    ### it will be assumed that the line numbers of the labels
    ### match the line numbers of the training data

    def readLabels(self, fileName, labelName):
        inFile = open (fileName, "r")

        lineList = []
        word = ''

        string = inFile.readline()

        while string:
            labelName.append (string[0])
            string = inFile.readline()
        inFile.close()

    ### end readLabels

    ### initializeWeight function
    def initializeWeight (self):
        self.m = len(self.vocabulary)
        self.w = np.zeros(self.m, dtype=int)
        self.wCache = np.zeros(self.m, dtype=int)
    ### end initializeWeight function

    ### perceptron function:

    def perceptron (self):
        ### initialize variables
        ### initialize prediction (yHat) and actual (yStar) to (0)
        ### use numpy for vectors
        ### create a numpy array of zeroes the size of m for weight, w
        #m = len(self.vocabulary)

        for iteration in range(self.maxIteration):
            mistakes = 0
            yHat = 0
            yStar = 0

            for fortune in self.featureVectorList:
                ### yHat and yStar are in the set {+1, -1}

                yStar = sign(int(fortune[0]))
                yHat = sign(self.w.dot(fortune[1]) )
                ### if the prediction doesn't match the label,
                ### update the weight
                if yHat != yStar:
                    self.w = self.w + (self.eta * yStar * np.array(fortune[1]) )
                    mistakes += 1

            numTrain = len(self.featureVectorList)
            numTest = len(self.testVectorList)

            trainMistakes = self.checkAccuracy(self.featureVectorList)
            testMistakes = self.checkAccuracy(self.testVectorList)

            self.numberOfMistakes.append(mistakes)
            self.standardTrainingAccuracy.append(100 - (100 * (float(trainMistakes)/numTrain)))
            self.standardTestingAccuracy.append(100 - (100 * (float(testMistakes))/numTest))

            '''
            print 'iteration: ', iteration + 1
            print 'Training mistakes: ', trainMistakes, '   Testing mistakes: ', testMistakes
            print 'Training percentage: ', 100 - (100 * (float(trainMistakes)/numTrain)), '%', \
            '   Testing percentage: ', 100 - (100 * (float(testMistakes))/numTest), '%'
            '''

            #print self.w

    ### end perceptron

    ### avgPerceptron function:

    def avgPerceptron (self):
        ### initialize variables
        ### initialize prediction (yHat) and actual (yStar) to (0)
        ### use numpy for vectors
        ### create a numpy array of zeroes the size of m for weight, w
        #m = len(self.vocabulary)

        yHat = 0
        yStar = 0

        count = 1

        for iteration in range (self.maxIteration):

            for fortune in self.featureVectorList:
                ### yHat and yStar are in the set {+1, -1}

                yStar = sign(int(fortune[0]))
                yHat = sign(self.w.dot(fortune[1]) )
                ### if the prediction doesn't match the label,
                ### update the weight
                if yHat != yStar:
                    self.w = self.w + (self.eta * yStar * np.array(fortune[1]) )
                    self.wCache = self.wCache + (self.eta * yHat * np.array(fortune[1]))

                count += 1

            numTrain = len(self.featureVectorList)
            numTest = len(self.testVectorList)

            trainMistakes = self.checkAccuracy(self.featureVectorList)
            testMistakes = self.checkAccuracy(self.testVectorList)

            self.averagedTrainingAccuracy.append(100 - (100 * (float(trainMistakes)/numTrain)))
            self.averagedTestingAccuracy.append(100 - (100 * (float(testMistakes))/numTest))

            '''
            print 'iteration: ', iteration + 1
            print 'Training mistakes: ', trainMistakes, '   Testing mistakes: ', testMistakes
            print 'Training percentage: ', 100 - (100 * (float(trainMistakes)/numTrain)), '%', \
            '   Testing percentage: ', 100 - (100 * (float(testMistakes))/numTest), '%'
            '''

        '''
        for vector in range(len(self.wCache)):
            for element in self.wCache[vector][1]:
                newWeight = float(element) / count
                self.wCache[vector][1][element] = newWeight
            print 'weight: ', self.wCache[vector][1]
        '''
        self.wCache = self.wCache / count
        #print self.w

    ### end avgPerceptron

    ### Check accuracy:
    def checkAccuracy (self, dataName):
        error = 0
        for fortune in dataName:
            ### yHat and yStar are in the set {+1, -1}

            yStar = sign(int(fortune[0]))
            yHat = sign(self.w.dot(fortune[1]) )
            ### if the prediction doesn't match the label,
            ### update the weight
            if yHat != yStar:
                error += 1

        return error

    ### end checkAccuracy function

    ### Check averaged accuracy:
    def checkAvgAccuracy (self):
        error = 0
        for fortune in self.featureVectorList:
            ### yHat and yStar are in the set {+1, -1}

            yStar = sign(int(fortune[0]))
            yHat = sign(self.wCache.dot(fortune[1]) )
            ### if the prediction doesn't match the label,
            ### update the weight
            if yHat != yStar:
                error += 1

        return error

    ### end checkAvgAccuracy function
