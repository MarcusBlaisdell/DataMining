########################
### Marcus Blaisdell
### Cpt_S 315
### Final Project
###
### Functions.py
###
########################

### buildVocabulary function
### create a list of all words present in the training data
### in alphabetical order

def buildVocabulary (trainData, stopList):
    masterDict = {}

    for line in trainData:
        for word in line:
                ### only add if it's not in the stopList
            if stopList.get(word, 'n') == 'n':
                    ### only add if it's not already in the dictionary
                if masterDict.get(word, 'n') == 'n':
                    masterDict[word] = 1

        ### make a list from the dictionary keys
    vocabulary = masterDict.keys()
        ### alphabetize the list:
    vocabulary.sort()

    return vocabulary
### end buildVocabulary


### buildFeatureList function
### create a list of feature vectors for each line
### in trainData

def buildFeatureList (vocabulary, trainData):
    featureList = []
    m = len(vocabulary)
    index = 0
    excludeDict = {' ':1, ',':1, '.':1, ';':1, ':':1, '"':1, '!':1, '?':1, '\'':1}

    for line in trainData:
        featureVector = [0] * m
        featureTuple = []

        word = ''
        wordList = []
        tempVocab = {}

        for character in range (len(line[1])):
            if excludeDict.get (line[1][character], '--') != '--':
                word = str.lower(word)

                if tempVocab.get(word, '--') == '--':
                    tempVocab[word] = 1
                word = ''
            else:
                word += line[1][character]

        wordList = tempVocab.keys()
        for word in wordList:
            try:
                if featureVector[vocabulary.index(word)] == 0:
                    featureVector[vocabulary.index(word)] = 1
            except:
                pass

        featureTuple = [trainData[index][2], featureVector]
        featureList.append(featureTuple)
        index += 1

    return featureList


### end buildFeatureList

### build noun list:
def buildNoun (fileName):
    nounList = []
    inFile = open (fileName, "r")

    string = inFile.readline ()

    while string:
        word = ''
        for i in range (len(string)):
            word += string[i]

        nounList.append (word)
        string = inFile.readline ()

    inFile.close ()

    return nounList
### end buildNoun function

### build List:
def buildList (fileName):
    listName = []
    inFile = open (fileName, "r")

    string = inFile.readline ()

    while string:
        word = ''
        if len(string) > 2:
            for i in range (len(string)):
                word += string[i]

            listName.append(word)
        string = inFile.readline ()

    inFile.close ()

    return listName
### end buildList function

### sign function, return +1 if value is > 0,
### return -1 if it is <= 0

def sign(value):
    if value > 0:
        return 1
    else:
        return -1

### end sign function

### create .arff file

def createARFF (outputFile, vocabulary, featureVectorList):
    outFile = open (outputFile, "w")
    ### format header:
    outFile.write (str('@relation spooky'))
    outFile.write ('\n')
    for word in vocabulary:
        outFile.write ('@attribute \'')
        outFile.write (word)
        outFile.write ('\' {0,1}')
        outFile.write ('\n')

    outFile.write ('@attribute Class { \'EAP\', \'MWS\', \'HPL\'}')
    outFile.write ('\n')

    outFile.write ('@data')
    outFile.write ('\n')

    for record in featureVectorList:
        for word in record[1]:
            outFile.write (str(word))
            outFile.write (',')
        outFile.write ('\'')
        outFile.write (record[0])
        outFile.write ('\'\n')

    outFile.close()

    ### end createARFF function
