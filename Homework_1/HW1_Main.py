'''
Marcus Blaisdell
CptS 315
Homework #1
2/8/18
Professor Jana Doppa

HW1_Main.py

This file is the main program
'''

from HW1_Prep import *

support = 100

### format textfile to a python list:

inputList = getList ()

### create an indexable table of unique items from
### baskets in inputList:

uniqueItems = createTableOne(inputList)

### count items:

uniqueCount = pass1(inputList, uniqueItems)

### get a list of indexes that have counts
### greater-than-equal-to the support level

frequentItems = filter1(uniqueCount, support)

### get a list of pairs:

pairs = pass2(inputList, uniqueItems, uniqueCount, support, frequentItems)

### get a list of triples:

triples = pass3(inputList, uniqueItems, uniqueCount, support, frequentItems)

### Generate scores for pairs and triples:

pairScoresXY =  calcConfidencesXY (uniqueCount, pairs, len(inputList), uniqueItems)
pairScoresYX =  calcConfidencesYX (uniqueCount, pairs, len(inputList), uniqueItems)

tripleScoreXYZ = calcConfidencesXYZ (uniqueCount, triples, len(inputList), uniqueItems)
tripleScoreXZY = calcConfidencesXZY (uniqueCount, triples, len(inputList), uniqueItems)
tripleScoreYZX = calcConfidencesYZX (uniqueCount, triples, len(inputList), uniqueItems)

### sort by score:

mergeSort(pairScoresXY)
mergeSort(pairScoresYX)
mergeSort(tripleScoreXYZ)
mergeSort(tripleScoreXZY)
mergeSort(tripleScoreYZX)

### We are only interested in the top 5 from each:

del pairScoresXY[5:]
del pairScoresYX[5:]
del tripleScoreXYZ[5:]
del tripleScoreXZY[5:]
del tripleScoreYZX[5:]

### if two tuples have the same score, order them lexicographically:

fixOrder (pairScoresXY)
fixOrder (pairScoresYX)
fixOrder (tripleScoreXYZ)
fixOrder (tripleScoreXZY)
fixOrder (tripleScoreYZX)

### write the output to text file:

outFile = open('output.txt', 'w')

outFile.write ('OUTPUT A: ')
outFile.write ('\n')

for x in range (5):
    outFile.write (pairScoresXY[x][0][0])
    outFile.write (' ')
    outFile.write (pairScoresXY[x][0][1])
    outFile.write (' ')
    outFile.write (str(pairScoresXY[x][1]))
    outFile.write ('\n')

for x in range (5):
    outFile.write (pairScoresYX[x][0][0])
    outFile.write (' ')
    outFile.write (pairScoresYX[x][0][1])
    outFile.write (' ')
    outFile.write (str(pairScoresYX[x][1]))
    outFile.write ('\n')

outFile.write ('OUTPUT B: ')
outFile.write ('\n')

for x in range (5):
    outFile.write (tripleScoreXYZ[x][0][0])
    outFile.write (' ')
    outFile.write (tripleScoreXYZ[x][0][1])
    outFile.write (' ')
    outFile.write (tripleScoreXYZ[x][0][2])
    outFile.write (' ')
    outFile.write (str(tripleScoreXYZ[x][1]))
    outFile.write ('\n')

for x in range (5):
    outFile.write (tripleScoreXZY[x][0][0])
    outFile.write (' ')
    outFile.write (tripleScoreXZY[x][0][1])
    outFile.write (' ')
    outFile.write (tripleScoreXZY[x][0][2])
    outFile.write (' ')
    outFile.write (str(tripleScoreXZY[x][1]))
    outFile.write ('\n')

for x in range (5):
    outFile.write (tripleScoreYZX[x][0][0])
    outFile.write (' ')
    outFile.write (tripleScoreYZX[x][0][1])
    outFile.write (' ')
    outFile.write (tripleScoreYZX[x][0][2])
    outFile.write (' ')
    outFile.write (str(tripleScoreYZX[x][1]))
    outFile.write ('\n')

outFile.close()
