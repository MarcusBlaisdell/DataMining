########################
### Marcus Blaisdell
### Cpt_S 315
### Homework #3
###
### HW3_FC_Class.py
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

def buildFeatureList (vocabulary, trainData, trainLabel):
    featureList = []
    m = len(vocabulary)
    #featureVector = [0] * m
    #featureTuple = []
    index = 0

    for line in trainData:
        featureVector = [0] * m
        featureTuple = []
        for word in line:
            try:
                if featureVector[vocabulary.index(word)] == 0:
                    featureVector[vocabulary.index(word)] = 1
            except:
                pass
        featureTuple = [trainLabel[index][0], featureVector]
        featureList.append(featureTuple)
        index += 1

    return featureList


### end buildFeatureList


### sign function, return +1 if value is > 0,
### return -1 if it is <= 0

def sign(value):
    if value > 0:
        return 1
    else:
        return -1

### end sign function
