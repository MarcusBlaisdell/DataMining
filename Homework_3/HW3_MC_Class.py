########################
### Marcus Blaisdell
### Cpt_S 315
### Homework #3
###
### HW3_MC_Class.py
###
########################

########################
###
### 1. initialize the weights w1 = 0, w2 = 0, ... wk = 0
### 2. for each training iteration, do:
### 3.    for each training example, do:
### 4.       yHat = argmax y in the set {1, 2, ..., k} wy * xt // predict using current weights
### 5.       if mistake then:
### 6.          wyt = wyt + eta * xt // update the weights
### 7.          wyhatt = wyhatt - eta * xt // update the weights
### 8.       end if
### 9.    end for
### 10. end for
### 11. return final weight vectors w1, w2, ..., wk
###
########################

import numpy as np
from HW3_Functions import sign
from string import ascii_lowercase

class OCR ():
    featureVectorList = []
    testVectorList = []
    labelListDict = {}
    labelList = []
    weightVectors = []
    weightVectorsCache = []
    eta = 1
    maxIteration = 20
    numberOfMistakes = []
    standardTrainingAccuracy = []
    standardTestingAccuracy = []
    averagedTrainingAccuracy = []
    averagedTestingAccuracy = []

    def __init__(self):
        pass

    ### end __init__ functions
    def readData(self, fileName, dataName):
        string = ''

        inFile = open (fileName, "r")

        string = inFile.readline()
        while string:
            index = 0
            featureVector = [0] * 128
            label = ''
            featureTuple = []

            ### if the line size is less than the size of a feature vector,
            ### it cannot contain a feature vector, so skip it:
            if len(string) < 128:
                pass
            else:
                ### move to the beginning of the data, it comes after the 'im' string
                while string[index] != 'i' and string[index + 1] != 'm':
                    index += 1

                ### move index to after the 'im' string
                index += 2

                ### populate the featureVector
                for x in range(index, index + 128):
                    featureVector[x - index] = int(string[x])

                ### get the feature label:
                label = string[index + 129]

                ### package the data in a list:
                featureTuple = [label, featureVector]

                ### add the feature vector to the feature vector list:
                dataName.append (featureTuple)

            string = inFile.readline()

    ### end readData

    ### build a label list from the ascii table:
    def buildLabelList(self):
        for letter in ascii_lowercase:
            if self.labelListDict.get(letter[0], '-') == '-':
                self.labelListDict[letter[0]] = 1

        ### create a list of the unique labels:
        self.labelList = self.labelListDict.keys()

        ### sort the list alphabetically
        self.labelList.sort()

    '''
    ### build a label list from the training data:
    def buildLabelList(self):
        ### read through each feature vector and read the label:
        ### add unique labels to a dictionary:
        for element in self.featureVectorList:
            if self.labelListDict.get(element[0], '-') == '-':
                self.labelListDict[element[0]] = 1

        ### create a list of the unique labels:
        self.labelList = self.labelListDict.keys()

        ### sort the list alphabetically
        self.labelList.sort()

    '''
    ### end buildLabelList function

    def buildWeightVectors(self):
        for label in self.labelList:
            w = np.zeros(128, dtype=int)
            weightTuple = [label, w]
            self.weightVectors.append(weightTuple)

        for label in self.labelList:
            w = np.zeros(128, dtype=int)
            weightTuple = [label, w]
            self.weightVectorsCache.append(weightTuple)

    ### end buildWeightVectors function

    ### perceptron function
    def perceptron (self):
        mistakes = 0

        ### for each iteration (step 2)
        ### iterate maxIteration times
        for iteration in range(self.maxIteration):

            ### for each training example (step 3)
            ### for each (xt, yt) in the set of D:
            for vectorList in self.featureVectorList:
                yStar = vectorList[0]
                yHatMax = 0
                maxWeight = 0
                yHat = ''

                ### need the index of the correct label from weightVectors:
                ### this is ugly***, it can be improved
                for listIndex in range(len(self.weightVectors)):
                    if self.weightVectors[listIndex][0] == yStar:
                        correctIndex = listIndex

                ### yHatt = argmax y in the set of weight vectors, k (step 4) (26 total weight vectors)
                ### find the weight vector with the highest score:
                for weight in range (len(self.weightVectors)):
                    yHatk = self.weightVectors[weight][1].dot( np.array(vectorList[1]) )
                    if weight == 0:
                        yHatMax = yHatk
                        ### initialize to the first weight vector:
                        yHat = self.weightVectors[0][0]

                    if yHatk > yHatMax:
                        yHatMax = yHatk
                        maxWeight = weight
                        yHat = self.weightVectors[maxWeight][0]

                ### if prediction is incorrect, update the weights:
                if yHat != yStar:
                    tempArray1 = self.weightVectors[correctIndex][1] + self.eta * np.array(vectorList[1])
                    tempArray2 = self.weightVectors[maxWeight][1] - self.eta * np.array(vectorList[1])
                    self.weightVectors[correctIndex][1] = tempArray1
                    self.weightVectors[maxWeight][1] = tempArray2
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
            print 'Training percentage: ', 100 - (100 * (float(trainMistakes)/numTrain)), '%', '   \
            Testing percentage: ', 100 - (100 * (float(testMistakes))/numTest)
            '''

        #for weight in self.weightVectors:
            #print weight[1]

    ### end perceptron function

    ### averaged perceptron function
    def avgPerceptron (self):
        count = 1

        for iteration in range(self.maxIteration):

            ### for each (xt, yt) in the set of D:
            for vectorList in self.featureVectorList:
                yStar = vectorList[0]
                yHatMax = 0
                maxWeight = 0
                yHat = ''

                ### need the index of the correct label from weightVectors:
                ### this is ugly***, it can be improved
                for listIndex in range(len(self.weightVectorsCache)):
                    if self.weightVectors[listIndex][0] == yStar:
                        correctIndex = listIndex

                ### find the weight vector with the highest score:
                for weight in range (len(self.weightVectors)):
                    yHatk = self.weightVectors[weight][1].dot( np.array(vectorList[1]) )
                    if weight == 0:
                        yHatMax = yHatk
                        ### initialize to the first weight vector:
                        yHat = self.weightVectors[0][0]
                    #print 'weight: ', weight, ' yHatk: ', yHatk

                    if yHatk > yHatMax:
                        yHatMax = yHatk
                        maxWeight = weight
                        yHat = self.weightVectors[maxWeight][0]

                ### if prediction is incorrect, update the weights:
                if yHat != yStar:
                    tempArray1 = self.weightVectors[correctIndex][1] + self.eta * np.array(vectorList[1])
                    tempArray2 = self.weightVectors[maxWeight][1] - self.eta * np.array(vectorList[1])
                    self.weightVectors[correctIndex][1] = tempArray1
                    self.weightVectors[maxWeight][1] = tempArray2
                    tempArray3 = self.weightVectorsCache[correctIndex][1] + (count * self.weightVectors[correctIndex][1])
                    tempArray4 = self.weightVectorsCache[maxWeight][1] - (count * self.weightVectors[maxWeight][1])
                    #tempArray3 = self.weightVectorsCache[maxWeight][1] + ( self.weightVectors[maxWeight][1].dot(count * self.weightVectorsCache[maxWeight][1] ))
                    self.weightVectorsCache[correctIndex][1] = tempArray3
                    self.weightVectorsCache[maxWeight][1] = tempArray4


                count += 1
        ### end iteration loop

            numTrain = len(self.featureVectorList)
            numTest = len(self.testVectorList)

            trainMistakes = self.checkAvgAccuracy(self.featureVectorList)
            testMistakes = self.checkAvgAccuracy(self.testVectorList)

            self.averagedTrainingAccuracy.append(100 - (100 * (float(trainMistakes)/numTrain)))
            self.averagedTestingAccuracy.append(100 - (100 * (float(testMistakes))/numTest))
            '''
            print 'iteration: ', iteration + 1
            print 'Training mistakes: ', trainMistakes, '   Testing mistakes: ', testMistakes
            print 'Training percentage: ', 100 - (100 * (float(trainMistakes)/numTrain)), '%', \
            '   Testing percentage: ', 100 - (100 * (float(testMistakes))/numTest)
            '''
        '''
        for vector in range(len(self.weightVectorsCache)):
            for element in self.weightVectorsCache[vector][1]:
                newWeight = float(element) / count
                self.weightVectorsCache[vector][1][element] = newWeight
            print 'weight: ', self.weightVectorsCache[vector][1]
        '''

    ### end avgPerceptron function


    ### checkAccuracy function
    def checkAccuracy (self, dataName):
        yHatMax = 0
        mistakes = 0
        maxWeight = 0
        yHat = ''

        ### for each (xt, yt) in the set of D:
        for vectorList in dataName:
            yStar = vectorList[0]
            ### need the index of the correct label from weightVectors:
            ### this is ugly***, it can be improved
            for listIndex in range(len(self.weightVectors)):
                if self.weightVectors[listIndex][0] == yStar:
                    correctIndex = listIndex

            yHat = self.weightVectors[0][0]
            ### find the weight vector with the highest score:
            for weight in range (len(self.weightVectors)):
                yHatk = self.weightVectors[weight][1].dot( np.array(vectorList[1]) )
                if weight == 0:
                    yHatMax = yHatk
                    ### initialize to the first weight vector:
                    yHat = self.weightVectors[0][0]


                if yHatk >= yHatMax:
                    yHatMax = yHatk
                    maxWeight = weight
                    yHat = self.weightVectors[maxWeight][0]

            ### if prediction is incorrect, update the mistake count:
            if yHat != yStar:
                mistakes += 1

        return mistakes
    ### end checkAccuracy function

    ### checkAvgAccuracy function
    def checkAvgAccuracy (self, dataName):
        yHatMax = 0
        mistakes = 0
        maxWeight = 0
        yHat = ''

        ### for each (xt, yt) in the set of D:
        for vectorList in dataName:
            yStar = vectorList[0]
            ### need the index of the correct label from weightVectorsCache:
            ### this is ugly***, it can be improved
            for listIndex in range(len(self.weightVectorsCache)):
                if self.weightVectorsCache[listIndex][0] == yStar:
                    correctIndex = listIndex

            yHat = self.weightVectorsCache[0][0]
            ### find the weight vector with the highest score:
            for weight in range (len(self.weightVectorsCache)):
                yHatk = self.weightVectorsCache[weight][1].dot( np.array(vectorList[1]) )
                if weight == 0:
                    yHatMax = yHatk
                    ### initialize to the first weight vector:
                    yHat = self.weightVectorsCache[0][0]


                if yHatk >= yHatMax:
                    yHatMax = yHatk
                    maxWeight = weight
                    yHat = self.weightVectorsCache[maxWeight][0]

            ### if prediction is incorrect, update the mistake count:
            if yHat != yStar:
                mistakes += 1

        return mistakes
    ### end checkAccuracy function

    ### print the bitmaps of data:
    def printBitMaps(self):
        for character in self.featureVectorList:
            print '=='
            print character[0]
            i = 0
            while i < 128:
                string = ''
                for j in range (8):
                    if character[1][i] == 1:
                        string += '*'
                    else:
                        string += ' '
                    i += 1
                print string

    ### end printBitMaps function
