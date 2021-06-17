########################
### Marcus Blaisdell
### Cpt_S 315
### Final Project
###
### A_Class.py
### Multi-class Classifier
###
########################

########################
### 1. initialize the weights, w = 0
### 2. for each training iteration, do:
### 3.    for each training example, do:
### 4.       yHat = max{(wlabel*xt) } // predict using current weights
### 5.       if mistake, then
###             // update the weights
### 6.          wcorrect = w + eta * xt
###             wincorrect = w - eta * xt
### 7.       end if
### 8.    end for
### 9. end for
###
########################

import numpy as np
from Functions import sign

class AClass():
    ### attributes:
        # dictionary let's us utilize the hash functions for faster searching
    stopList = {}
        # lists to utilize indexing:
    trainData = []
    testData = []
    vocabulary = []
    featureVectorList = []
    testVectorList = []
    eta = 1 # learning ratingIndex
    w = np.array([0]) # weight vector
    wList = []
    fwList = []
    wCache = np.array([0]) # cached weight vector
    m = 0
    maxIteration = 20
    numberOfMistakes = []
    standardTrainingAccuracy = []
    standardTestingAccuracy = []
    averagedTrainingAccuracy = []
    averagedTestingAccuracy = []
    wordList = {}
    weightList = {}
    frequencyList = []
    header = []
    excludeChars = {' ':1, ',':1, '.':1, '"':1, ';':1, ':':1, '!':1, '?':1, '\'':1 }
    MWSfreq = {}
    EAPfreq = {}
    HPLfreq = {}


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

    ### read the file into a list for processing:

    def readLines(self, fileName, dataName):
        inFile = open (fileName, "r")

        lineList = []
        tempTuple = []
        quoteFlag = 0
        tuplePos = 0
        tempString = ''

        string = inFile.readline()

        ### First line is header, skip it:

        string = inFile.readline()

        ### The rest of the lines are data:

        while string:
            r_id = ''
            sentence = ''
            author = ''

            ### The id and author book-end the sentence
            ### so it's easier to use the start and end points
            ### for indexing because sometimes sentences have
            ### quotes in them that prevent me from using that
            ### as a delimiter
            ### id and author fields are fixed-width, so this works
            ### as long as they stay the same size, they are consistent
            ### in this input file
            for character in range (1,8):
                r_id += string[character]
            for character in range (11, len(string) - 8):
                sentence += str.lower(string[character])
            for character in range (len(string) - 5, len(string) - 2):
                author += string[character]
            tempTuple = [r_id, sentence, author]
            '''
            ### This will create a list of words in the sentence
            sentenceList = []
            word = ''
            for character in range (len(sentence)):
                if self.excludeChars.get (sentence[character], '--') != '--':
                    word = str.lower(word)
                    if self.stopList.get(word, '--') == '--':
                        sentenceList.append(word)

                    word = ''
                else:
                    word += sentence[character]
            #tempTuple = [r_id, sentenceList, author]
            ###
            #for word in sentenceList:
                #self.wordFrequency ()
            '''
            dataName.append (tempTuple)

            string = inFile.readline()

        inFile.close()

    ### end readLines

    ### word Frequency by author
    def wordFrequency (self, word, author):


        if author == "MWS":
            if self.MWSfreq.get(word, '--') == '--':
                self.MWSfreq[word] = 1
            else:
                self.MWSfreq[word] += 1
        if author == "EAP":
            if self.EAPfreq.get(word, '--') == '--':
                self.EAPfreq[word] = 1
            else:
                self.EAPfreq[word] += 1
        if author == "HPL":
            if self.HPLfreq.get(word, '--') == '--':
                self.HPLfreq[word] = 1
            else:
                self.HPLfreq[word] += 1

    ### end wordFrequency function
    '''
    ### get word list, experimental:
    def createWordList (self):
        commaCount = 0
        newArray = ''
        word = ''

        ### parse words into a dictionary:
        for line in self.trainData:
            for word in line[1]:
                if self.wordList.get(word, '--') == '--':
                    self.wordList[word] = 1

                    word = ''

        ### move words into alphabetized list
        self.vocabulary = self.wordList.keys()
        self.vocabulary.sort()

    ### end createWordList function
    '''
    ### get word list:
    def createWordList (self):
        commaCount = 0
        newArray = ''
        word = ''

        ### parse words into a dictionary:
        for line in self.trainData:
            for character in range (len(line[1])):
                if self.excludeChars.get (line[1][character], '--') != '--':
                    word = str.lower(word)
                    if self.stopList.get(word, '--') != '--':
                        if self.wordList.get(word, '--') == '--':
                            self.wordList[word] = 1
                    self.wordFrequency(word, line[2])
                    word = ''
                else:
                    word += line[1][character]

        ### move words into alphabetized list
        self.vocabulary = self.wordList.keys()
        self.vocabulary.sort()

    ### end createWordList function

    ### initializeWeight function
    def initializeWeight (self):
        ### first, build list of classifiers:
        for line in self.trainData:
            if self.weightList.get (line[2], "--") == "--":
                self.weightList[line[2]] = 1

        ### get the size of the vocabulary to build the weight vectors
        ### the correct size:
        self.m = len(self.vocabulary)

        weightListList = self.weightList.keys ()

        for classifier in weightListList:
            weightTuple = np.zeros(self.m, dtype=int)
            wListElement = [classifier, weightTuple]
            self.wList.append (wListElement)
            self.fwList.append(wListElement)
            #self.wList.get[] = np.zeros(self.m, dtype=int)
        self.wCache = np.zeros(self.m, dtype=int)
    ### end initializeWeight function

    ### perceptron function:

    def perceptron (self):
        minScore = 100
        maxScore = 0

        for iteration in range(self.maxIteration):
            mistakes = 0
            yHatScore = 0
            yHat = ''
            yHatMax = 0
            yHatMaxIndex = 0
            yStar = ''

            for line in self.featureVectorList:
                ### yStar is author

                yHatScore = 0
                yHatMax = 0
                yHatMaxIndex = 0
                yHat = self.wList[0][0]
                yStar = line[0]

                ### get the index for the correct weight:
                for index in range(len(self.wList)):
                    if yStar == self.wList[index][0]:
                        yStarIndex = index

                for index in range(len(self.wList)):
                    yHatScore = np.array(self.wList[index][1]).dot(np.array(line[1]))

                    if yHatScore > yHatMax:
                        yHatMax = yHatScore
                        yHatMaxIndex = index
                        yHat = self.wList[index][0]

                ### if the prediction doesn't match the label,
                ### update the weight
                if yHat != yStar:
                    #print "Incorrect, updating: " + yHat + yStar
                    self.wList[yStarIndex][1] = np.array(self.wList[yStarIndex][1]) + self.eta * np.array(line[1])
                    self.wList[yHatMaxIndex][1] = np.array(self.wList[yHatMaxIndex][1]) - self.eta * np.array(line[1])
                    mistakes += 1
                #else:
                    #print "correct: " + yHat + yStar
            #print "mistakes = " + str(mistakes)

            numTrain = len(self.featureVectorList)
            numTest = len(self.testVectorList)

            trainMistakes = self.checkAccuracy(self.featureVectorList)
            testMistakes = self.checkAccuracy(self.testVectorList)

            self.numberOfMistakes.append(mistakes)
            self.standardTrainingAccuracy.append(100 - (100 * (float(trainMistakes)/numTrain)))
            self.standardTestingAccuracy.append(100 - (100 * (float(testMistakes))/numTest))


            print 'iteration: ', iteration + 1
            #print 'Training mistakes: ', trainMistakes
            print 'Training mistakes: ', trainMistakes, '   Testing mistakes: ', testMistakes
            #print 'Training percentage: ', 100 - (100 * (float(trainMistakes)/numTrain)), '%'

            trainPercent = 100 - (100 * (float(trainMistakes)/numTrain))
            testPercent = 100 - (100 * (float(testMistakes))/numTest)
            if trainPercent > maxScore:
                maxScore = trainPercent
            if trainPercent < minScore:
                minScore = trainPercent
            print 'Training percentage: ', trainPercent, '%', \
            '   Testing percentage: ', testPercent, '%'


            #print self.w
        print "lowest: ", minScore, '%'
        print "highest: ", maxScore, '%'

    ### end perceptron

    ### perceptron function:

    def perceptronFreq (self):
        for x in self.fwList:
            print x
        minScore = 100
        maxScore = 0

        for iteration in range(self.maxIteration):
            mistakes = 0
            yHatScore = 0
            yHat = ''
            yHatMax = 0
            yHatMaxIndex = 0
            yStar = ''

            for line in self.featureVectorList:
                ### yStar is author

                yHatScore = 0
                yHatMax = 0
                yHatMaxIndex = 0
                yHat = self.fwList[0][0]
                yStar = line[0]

                ### get the index for the correct weight:
                for index in range(len(self.fwList)):
                    if yStar == self.fwList[index][0]:
                        yStarIndex = index

                for index in range(len(self.fwList)):
                    yHatScore = np.array(self.fwList[index][1]).dot(np.array(line[1]))

                    if yHatScore > yHatMax:
                        yHatMax = yHatScore
                        yHatMaxIndex = index
                        yHat = self.fwList[index][0]

                ### if the prediction doesn't match the label,
                ### update the weight
                if yHat != yStar:
                    #print "Incorrect, updating: " + yHat + yStar
                    self.fwList[yStarIndex][1] = np.array(self.fwList[yStarIndex][1]) + self.eta * np.array(line[1])
                    self.fwList[yHatMaxIndex][1] = np.array(self.fwList[yHatMaxIndex][1]) - self.eta * np.array(line[1])
                    mistakes += 1
                #else:
                    #print "correct: " + yHat + yStar
            #print "mistakes = " + str(mistakes)

            numTrain = len(self.featureVectorList)
            numTest = len(self.testVectorList)

            trainMistakes = self.checkAccuracy(self.featureVectorList)
            testMistakes = self.checkAccuracy(self.testVectorList)

            self.numberOfMistakes.append(mistakes)
            self.standardTrainingAccuracy.append(100 - (100 * (float(trainMistakes)/numTrain)))
            self.standardTestingAccuracy.append(100 - (100 * (float(testMistakes))/numTest))


            print 'iteration: ', iteration + 1
            #print 'Training mistakes: ', trainMistakes
            print 'Training mistakes: ', trainMistakes, '   Testing mistakes: ', testMistakes
            #print 'Training percentage: ', 100 - (100 * (float(trainMistakes)/numTrain)), '%'

            trainPercent = 100 - (100 * (float(trainMistakes)/numTrain))
            testPercent = 100 - (100 * (float(testMistakes))/numTest)
            if trainPercent > maxScore:
                maxScore = trainPercent
            if trainPercent < minScore:
                minScore = trainPercent
            print 'Training percentage: ', trainPercent, '%', \
            '   Testing percentage: ', testPercent, '%'


            #print self.w
        print "lowest: ", minScore, '%'
        print "highest: ", maxScore, '%'

    ### end perceptronFreq

    ### build frequency weight lists
    def buildFrequencyWeights (self):
        MWSList = self.MWSfreq.keys()

        for word in MWSList:
            try:
                self.fwList[0][1][self.vocabulary.index(word)] = self.MWSfreq.get(word)
            except:
                pass
        EAPList = self.EAPfreq.keys()
        for word in EAPList:
            try:
                self.fwList[1][1][self.vocabulary.index(word)] = self.EAPfreq.get(word)
            except:
                pass
        HPLList = self.HPLfreq.keys()
        for word in HPLList:
            try:
                self.fwList[2][1][self.vocabulary.index(word)] = self.HPLfreq.get(word)
            except:
                pass

    ### end buildFrequencyWeights function

    ### prediction based on word frequency
    def frequencyPrediction (self):
        MWS_count = 0
        EAP_count = 0
        HPL_count = 0
        trainMistakes = 0
        testMistakes = 0

        for line in self.featureVectorList:
            MWSscore = 0
            EAPscore = 0
            HPLscore = 0
            yStar = line[0]
            for word in range(len(line[1])):
                if line[1][word] == 1:
                    MWSscore = self.MWSfreq.get(self.vocabulary[word])
                    EAPscore = self.EAPfreq.get(self.vocabulary[word])
                    HPLscore = self.HPLfreq.get(self.vocabulary[word])
                if MWSscore > EAPscore and MWSscore > HPLscore:
                    MWS_count += 1
                if EAPscore > MWSscore and EAPscore > HPLscore:
                    EAP_count += 1
                if HPLscore > EAPscore and HPLscore > MWSscore:
                    HPL_count += 1
            if MWS_count > EAP_count and MWS_count > HPL_count:
                yHat = 'MWS'
            if EAP_count > MWS_count and EAP_count > HPL_count:
                yHat = 'EAP'
            if HPL_count > EAP_count and HPL_count > MWS_count:
                yHat = 'HPL'

            if yStar != yHat:
                #self.wList[yStarIndex][1] = np.array(self.wList[yStarIndex][1]) + self.eta * np.array(line[1])
                #self.wList[yHatMaxIndex][1] = np.array(self.wList[yHatMaxIndex][1]) - self.eta * np.array(line[1])
                trainMistakes += 1

        numTrain = len(self.featureVectorList)
        trainPercent = 100 - (100 * float(trainMistakes) / numTrain)
        print 'Training mistakes: ' + str(trainMistakes) + ' - percentage = ' + str(trainPercent) + '%'

        MWS_count = 0
        EAP_count = 0
        HPL_count = 0
        mistakes = 0

        for line in self.testVectorList:
            MWSscore = 0
            EAPscore = 0
            HPLscore = 0
            yStar = line[0]
            for word in range(len(line[1])):
                if line[1][word] == 1:
                    MWSscore = self.MWSfreq.get(self.vocabulary[word])
                    EAPscore = self.EAPfreq.get(self.vocabulary[word])
                    HPLscore = self.HPLfreq.get(self.vocabulary[word])
                if MWSscore > EAPscore and MWSscore > HPLscore:
                    MWS_count += 1
                if EAPscore > MWSscore and EAPscore > HPLscore:
                    EAP_count += 1
                if HPLscore > EAPscore and HPLscore > MWSscore:
                    HPL_count += 1
            if MWS_count > EAP_count and MWS_count > HPL_count:
                yHat = 'MWS'
            if EAP_count > MWS_count and EAP_count > HPL_count:
                yHat = 'EAP'
            if HPL_count > EAP_count and HPL_count > MWS_count:
                yHat = 'HPL'

            if yStar != yHat:
                #self.wList[yStarIndex][1] = np.array(self.wList[yStarIndex][1]) + self.eta * np.array(line[1])
                #self.wList[yHatMaxIndex][1] = np.array(self.wList[yHatMaxIndex][1]) - self.eta * np.array(line[1])
                testMistakes += 1

        numTest = len(self.testVectorList)
        print 'testMistakes: ' + str(testMistakes) + ' numTest: ' + str(numTest)
        testPercent = 100 - (100 * float(testMistakes) / numTest)
        print 'testing mistakes: ' + str(testMistakes) + ' - percentage = ' + str(testPercent) + '%'

    ### end frequencyPrediction function

    ### Check accuracy:
    def checkAccuracy (self, dataName):
        #print "checkAccuracy"
        error = 0
        mistakes = 0
        yHatScore = 0
        yHatMax = 0
        yHatMaxIndex = 0

        for line in dataName:
            ### yHat and yStar are in the set {+1, -1}

            yStar = line[0]
            yHat = self.wList[0][0]
            for index in range(len(self.wList)):
                yHatScore = np.array(self.wList[index][1]).dot(np.array(line[1]))

                if yHatScore > yHatMax:
                    #print "updating"
                    yHatMax = yHatScore
                    yHatMaxIndex = index
                    yHat = self.wList[index][0]

            ### if the prediction doesn't match the label,
            ### update the weight
            if yHat != yStar:
                #print "error" + yHat + yStar
                error += 1

        return error

    ### end checkAccuracy function
