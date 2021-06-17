'''
Marcus Blaisdell
CptS 315
Homework #1
2/8/18
Professor Jana Doppa

HW1_Prep.py
This file reads input from text file and creates
the table that is needed for the A-priori algorithm
It finds all unique items in an input file and
puts them in an indexed dictionary
'''

### Python 3.6

DEBUG = 1

### convert the text file to a python list for processing:

def getList():
    ### Open input file for reading:

    myFile = open("browsingdata.txt", "r")

    ### read the first line to get started

    myStr = myFile.readline()

    ### Declare the variables that will be used in the loop:
    ### inputList is the master list that will hold the individual lists
    ### lineList is the individual lists
    ### newStr is the new string that is generated as text is read character-by
    ### character from each line and parsed into separate strings to be added
    ### to the lineList

    inputList = []
    lineList = []
    newStr = ""

    ### Read until input is no longer valid:

    while myStr:
        for x in myStr:
            if x != ' ' and x != '\r' and x != '\n':
                newStr += x
            else:
                if newStr != "":
                    lineList.append(newStr)
                newStr = ""
        inputList.append(lineList)
        lineList = []
        myStr = myFile.readline()

    myFile.close()

    return inputList

### Create a list of unique items

def createTableOne(inputList):

    ### each x in inputList is a basket of items:
    ### each y in x is an item in a basket

    uniqueItems = []

    for x in inputList:
        for y in x:
            if y in uniqueItems:
                z = 0
            else:
                uniqueItems.append(y)

    return uniqueItems

def pass1(inputList, uniqueItems):

    ### first pass:
    ### read each string from each list,
    ### increment its count

    ### create empty list of size of uniqueItems:
    ### the index of uniqueCount will hold the count
    ### of items from uniqueItems[index]

    uniqueCount = []

    for x in range (len(uniqueItems)):
        uniqueCount.append(0)

    ### count each item:

    for basket in inputList:
        for item in basket:
            uniqueCount[uniqueItems.index(item)] += 1

    return uniqueCount

### create a list of indexes that have counts
### greater than or equal to the support level

def filter1(uniqueCount, support):
    frequentItems = []
    for x in range(len(uniqueCount)):
        if uniqueCount[x] >= support:
            frequentItems.append(x)
    return frequentItems

### pass2, for each item in a basket, if it is a frequent item,
### check if it is also a frequent pair
### for each additional item in the basket, check if it is a frequent item
### if it its, store that pair as a tuple and increase the count of that tuple
### in the pair-count table

def pass2(inputList, uniqueItems, uniqueCount, support, frequentItems):
    pairs = {}
    #i_index = 0
    for basket in inputList:
        #if (i_index % 100 == 0):
            #print (i_index)
        #i_index += 1
        j_index = len(basket)
        #for item in basket:
        for item in range(j_index):
            ### if the item count is greater than support:
            if (uniqueItems.index(basket[item]) in frequentItems):
                ### check if any of the other items in the basket are also
                ### frequent items
                for nextItem in range(item + 1, j_index):
                    ### my list of valid pairs is in the order [smallerindex, largerindex]
                    ### enforce order:
                    if (uniqueItems.index(basket[nextItem]) in frequentItems):
                        if uniqueItems.index(basket[item]) < uniqueItems.index(basket[nextItem]):
                            tempPair = (uniqueItems.index(basket[item]), uniqueItems.index(basket[nextItem]))
                        else:
                            tempPair = (uniqueItems.index(basket[nextItem]), uniqueItems.index(basket[item]))
                        if pairs.has_key(tempPair):
                            pairs[tempPair] += 1
                        else:
                            pairs[tempPair] = 1

    return pairs

### pass3, for each item in a basket, if it is a frequent item,
### check if it is also a frequent triple
### for each additional item in the basket, check if it is a frequent item
### if it its, store that triple as a tuple and increase the count of that tuple
### in the triple-count table

def pass3(inputList, uniqueItems, uniqueCount, support, frequentItems):
    triples = {}
    #i_index = 0
    for basket in inputList:
        #if (i_index % 100 == 0):
            #print (i_index)
        #i_index += 1
        j_index = len(basket)
        for item in range(j_index):
            ### if the item count is greater than support:
            if (uniqueItems.index(basket[item]) in frequentItems):
                ### check if any of the other items in the basket are also
                ### frequent items
                for nextItem in range(item + 1, j_index):
                    if (uniqueItems.index(basket[nextItem]) in frequentItems):
                        for nextNextItem in range (nextItem + 1, j_index):
                            if (uniqueItems.index(basket[nextItem]) in frequentItems):
                                if uniqueItems.index(basket[item]) < uniqueItems.index(basket[nextItem]) < uniqueItems.index(basket[nextNextItem]):
                                    tempTriple = (uniqueItems.index(basket[item]), uniqueItems.index(basket[nextItem]), uniqueItems.index(basket[nextNextItem]))
                                elif uniqueItems.index(basket[item]) < uniqueItems.index(basket[nextNextItem]) < uniqueItems.index(basket[nextItem]):
                                    tempTriple = (uniqueItems.index(basket[item]), uniqueItems.index(basket[nextNextItem]), uniqueItems.index(basket[nextItem]))
                                elif uniqueItems.index(basket[nextItem]) < uniqueItems.index(basket[item]) < uniqueItems.index(basket[nextNextItem]):
                                    tempTriple = (uniqueItems.index(basket[nextItem]), uniqueItems.index(basket[item]), uniqueItems.index(basket[nextNextItem]))
                                elif uniqueItems.index(basket[nextItem]) < uniqueItems.index(basket[nextNextItem]) < uniqueItems.index(basket[item]):
                                    tempTriple = (uniqueItems.index(basket[nextItem]), uniqueItems.index(basket[nextNextItem]), uniqueItems.index(basket[item]))
                                elif uniqueItems.index(basket[nextNextItem]) < uniqueItems.index(basket[item]) < uniqueItems.index(basket[nextItem]):
                                    tempTriple = (uniqueItems.index(basket[nextNextItem]), uniqueItems.index(basket[item]), uniqueItems.index(basket[nextItem]))
                                elif uniqueItems.index(basket[nextNextItem]) < uniqueItems.index(basket[nextItem]) < uniqueItems.index(basket[item]):
                                    tempTriple = (uniqueItems.index(basket[nextNextItem]), uniqueItems.index(basket[nextItem]), uniqueItems.index(basket[item]))
                                if triples.has_key(tempTriple):
                                    triples[tempTriple] += 1
                                else:
                                    triples[tempTriple] = 1
    return triples

### calculate the confidences of the pairs, X=>Y and Y=>X:

def calcConfidencesXY (uniqueCount, pairs, numBaskets, uniqueItems):
    pairConfidencesXY = []
    for x in pairs.keys():
        if pairs[x] >= 100:
            B = uniqueCount[x[1]]
            AB = pairs[x]
            PofB = B / float (numBaskets)
            PofAB = AB / float (numBaskets)
            score = PofAB / float (PofB)
            pairConfidencesXY.append([[uniqueItems[x[0]], uniqueItems[x[1]]], score])
            #pairConfidencesXY.append([x[0], score])
    return pairConfidencesXY

def calcConfidencesYX (uniqueCount, pairs, numBaskets, uniqueItems):
    pairConfidencesYX = []
    for x in pairs.keys():
        if pairs[x] >= 100:
            B = uniqueCount[x[0]]
            AB = pairs[x]
            PofB = B / float (numBaskets)
            PofAB = AB / float (numBaskets)
            score = PofAB / float (PofB)
            pairConfidencesYX.append([[uniqueItems[x[1]], uniqueItems[x[0]]], score])
    return pairConfidencesYX

### Calculate the scores of XY=>Z, XY=>Y, YZ=>X

def calcConfidencesXYZ (uniqueCount, triples, numBaskets, uniqueItems):
    tripleConfidencesXYZ = []
    for x in triples.keys():
        if triples[x] >= 100:
            B = uniqueCount[x[2]]
            AB = triples[x]
            PofB = B / float (numBaskets)
            PofAB = AB / float (numBaskets)
            score = PofAB / float (PofB)
            tripleConfidencesXYZ.append([[uniqueItems[x[0]], uniqueItems[x[1]], uniqueItems[x[2]]], score])
    return tripleConfidencesXYZ

def calcConfidencesXZY (uniqueCount, triples, numBaskets, uniqueItems):
    tripleConfidencesXZY = []
    for x in triples.keys():
        if triples[x] >= 100:
            B = uniqueCount[x[1]]
            AB = triples[x]
            PofB = B / float (numBaskets)
            PofAB = AB / float (numBaskets)
            score = PofAB / float (PofB)
            tripleConfidencesXZY.append([[uniqueItems[x[0]], uniqueItems[x[2]], uniqueItems[x[1]]], score])
    return tripleConfidencesXZY

def calcConfidencesYZX (uniqueCount, triples, numBaskets, uniqueItems):
    tripleConfidencesYZX = []
    for x in triples.keys():
        if triples[x] >= 100:
            B = uniqueCount[x[0]]
            AB = triples[x]
            PofB = B / float (numBaskets)
            PofAB = AB / float (numBaskets)
            score = PofAB / float (PofB)
            tripleConfidencesYZX.append([[uniqueItems[x[1]], uniqueItems[x[2]], uniqueItems[x[0]]], score])
    return tripleConfidencesYZX

### use mergeSort to sort the lists by score

def mergeSort(theList):
    newList = []

    if len(theList) > 1:
        left = theList[:len(theList) / 2]
        right = theList[len(theList) / 2:]

        mergeSort (left)
        mergeSort (right)

        i = 0
        j = 0
        k = 0

        while i < len(left) and j < len(right):
            if left[i][1] > right[j][1]:
                theList[k] = left[i]
                i += 1
                k += 1
            else:
                theList[k] = right[j]
                j += 1
                k += 1
        while i < len(left):
            theList[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            theList[k] = right[j]
            j += 1
            k += 1

### If two elements in the list have the same score,
### list them in lexicographic order:

def fixOrder (theList):
    for index in range(4):
        cell = 0
        pos = 0
        i = 0

        if theList[index][1] == theList[index + 1][1]:
            while theList[index][0][pos][i] <= theList[index + 1][0][pos][i] and pos < len(theList[index][0]):
                if i < len(theList[index][0][pos]) - 1:
                    i += 1
                else:
                    i = 0
                    pos += 1
            if pos < len(theList[index][0]):
                swap = theList[index]
                theList[index] = theList[index + 1]
                theList[index + 1] = swap
