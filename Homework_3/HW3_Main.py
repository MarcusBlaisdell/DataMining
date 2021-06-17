########################
### Marcus Blaisdell
### Cpt_S 315
### Homework #3
###
### HW3_Main.py
###
########################

from HW3_FC_Class import *
from HW3_MC_Class import *
from HW3_Functions import *

### Fortune Cookie Classifier
### create an instance of our class:
myFC = FCookie()

### read data from text files:
### build stop list:
myFC.readStops ("fortunecookiedata/stoplist.txt")
### get training data and labels:
myFC.readLines ("fortunecookiedata/traindata.txt", myFC.trainData)
myFC.readLabels ("fortunecookiedata/trainlabels.txt", myFC.trainLabel)
### get testing data and labels:
myFC.readLines ("fortunecookiedata/testdata.txt", myFC.testData)
myFC.readLabels ("fortunecookiedata/testlabels.txt", myFC.testLabel)

### create a vocabulary
myFC.vocabulary = buildVocabulary (myFC.trainData, myFC.stopList)

### create a feature vector list
myFC.featureVectorList = buildFeatureList (myFC.vocabulary, myFC.trainData, myFC.trainLabel)
myFC.testVectorList = buildFeatureList (myFC.vocabulary, myFC.testData, myFC.testLabel)

### test Fortune Cookie classifier

myFC.initializeWeight ()

myFC.featureVectorList = buildFeatureList (myFC.vocabulary, myFC.trainData, myFC.trainLabel)
myFC.testVectorList = buildFeatureList (myFC.vocabulary, myFC.testData, myFC.testLabel)

myFC.perceptron ()

numTrain = len(myFC.featureVectorList)
numTest = len(myFC.testVectorList)
trainError = myFC.checkAccuracy(myFC.featureVectorList)
testError = myFC.checkAccuracy(myFC.testVectorList)

#print myFC.w

### test Fortune Cookie classifier, averaged perceptron:

myFC.initializeWeight ()

myFC.featureVectorList = buildFeatureList (myFC.vocabulary, myFC.trainData, myFC.trainLabel)
myFC.testVectorList = buildFeatureList (myFC.vocabulary, myFC.testData, myFC.testLabel)

myFC.avgPerceptron ()

numTrain = len(myFC.featureVectorList)
numTest = len(myFC.testVectorList)
trainError = myFC.checkAccuracy(myFC.featureVectorList)
testError = myFC.checkAccuracy(myFC.testVectorList)

#print myFC.w

### end test Fortune Coookie Classifier

'''
### for troubleshooting:
print len(myFC.stopList)
print len(myFC.trainData)
print len(myFC.trainLabel)
print len(myFC.vocabulary)
print len(myFC.featureVectorList)
'''


### MultiClass classifier:

myMC = OCR()

myMC.readData ("OCRdata/OCR-data/ocr_train.txt", myMC.featureVectorList)
myMC.readData ("OCRdata/OCR-data/ocr_test.txt", myMC.testVectorList)
myMC.buildLabelList ()

### use standard perceptron:

myMC.buildWeightVectors ()

### print out the images of the characters:
#myMC.printBitMaps()

myMC.perceptron()

### Use averaged perceptron:

myMC.buildWeightVectors ()

myMC.avgPerceptron()

### print results to screen:
'''
print 'results:'
print ''

for mistakes in range (len(myFC.numberOfMistakes)):
    print 'iteration: ', mistakes, ' Number of mistakes: ', myFC.numberOfMistakes[mistakes]
    ' training Accuracy: ', myFC.standardTrainingAccuracy[mistakes], '% ', \
    ' testing Accuracy: ', myFC.standardTestingAccuracy[mistakes], '% '
for mistakes in range (len(myFC.numberOfMistakes)):
    print 'iteration: ', mistakes, ' training Accuracy: ', myFC.standardTrainingAccuracy[mistakes], '% ', \
    ' testing Accuracy: ', myFC.standardTestingAccuracy[mistakes], '% '
print 'testing Accuracy standard perceptron: ', myFC.standardTrainingAccuracy[len(myFC.standardTrainingAccuracy) - 1], \
' testing Accuracy averaged perceptron: ', myFC.averagedTestingAccuracy[len(myFC.averagedTestingAccuracy) - 1]

print ''

for mistakes in range (len(myMC.numberOfMistakes)):
    print 'iteration: ', mistakes, ' Number of mistakes: ', myMC.numberOfMistakes[mistakes]
    ' training Accuracy: ', myMC.standardTrainingAccuracy[mistakes], '% ', \
    ' testing Accuracy: ', myMC.standardTestingAccuracy[mistakes], '% '
for mistakes in range (len(myMC.numberOfMistakes)):
    print 'iteration: ', mistakes, ' training Accuracy: ', myMC.standardTrainingAccuracy[mistakes], '% ', \
    ' testing Accuracy: ', myMC.standardTestingAccuracy[mistakes], '% '
print 'testing Accuracy standard perceptron: ', myMC.standardTrainingAccuracy[len(myMC.standardTrainingAccuracy) - 1], \
' testing Accuracy averaged perceptron: ', myMC.averagedTestingAccuracy[len(myMC.averagedTestingAccuracy) - 1], '% '
'''
### print results to file:

outFile = open('output.txt', 'w')

outFile.write ('Fortune Cookie Classifier: \n\n')
outFile.write ('\n')

for mistakes in range (len(myFC.numberOfMistakes)):
    outFile.write ('iteration: ')
    outFile.write (str(mistakes + 1))
    outFile.write (' Number of mistakes: ')
    outFile.write (str(myFC.numberOfMistakes[mistakes]))
    outFile.write ('\n')

outFile.write ('standard perceptron: \n\n')
for mistakes in range (len(myFC.numberOfMistakes)):
    outFile.write ('iteration: ')
    outFile.write (str(mistakes))
    outFile.write (' training Accuracy: ')
    outFile.write (str('%.2f' % myFC.standardTrainingAccuracy[mistakes]))
    outFile.write ('% ')
    outFile.write (' testing Accuracy: ')
    outFile.write (str('%.2f' % myFC.standardTestingAccuracy[mistakes]))
    outFile.write ('% \n')

'''
outFile.write ('averaged perceptron: \n\n')
for mistakes in range (len(myFC.numberOfMistakes)):
    outFile.write ('iteration: ')
    outFile.write (str(mistakes))
    outFile.write (' training Accuracy: ')
    outFile.write (str('%.2f' % myFC.averagedTrainingAccuracy[mistakes]))
    outFile.write ('% ')
    outFile.write (' testing Accuracy: ')
    outFile.write (str('%.2f' % myFC.averagedTestingAccuracy[mistakes]))
    outFile.write ('% \n')
'''

outFile.write ('testing Accuracy standard perceptron: ')
outFile.write (str('%.2f' % myFC.standardTrainingAccuracy[len(myFC.standardTrainingAccuracy) - 1]))
outFile.write (' testing Accuracy averaged perceptron: ')
outFile.write (str('%.2f' % myFC.averagedTestingAccuracy[len(myFC.averagedTestingAccuracy) - 1]))
outFile.write ('%\n')

outFile.write ('\n')

outFile.write ('MultiClass Classifier: \n\n')

for mistakes in range (len(myMC.numberOfMistakes)):
    outFile.write ( 'iteration: ')
    outFile.write (str(mistakes + 1))
    outFile.write (' Number of mistakes: ')
    outFile.write (str(myMC.numberOfMistakes[mistakes]))
    outFile.write ('\n')

outFile.write ('standard perceptron: \n\n')
for mistakes in range (len(myMC.numberOfMistakes)):
    outFile.write ( 'iteration: ')
    outFile.write (str(mistakes + 1))
    outFile.write (' training Accuracy: ')
    outFile.write (str('%.2f' % myMC.standardTrainingAccuracy[mistakes]))
    outFile.write ('% ')
    outFile.write (' testing Accuracy: ')
    outFile.write (str('%.2f' % myMC.standardTestingAccuracy[mistakes]))
    outFile.write ('% \n')
'''
outFile.write ('averaged perceptron: \n\n')
for mistakes in range (len(myMC.numberOfMistakes)):
    outFile.write ( 'iteration: ')
    outFile.write (str(mistakes + 1))
    outFile.write (' training Accuracy: ')
    outFile.write (str('%.2f' % myMC.averagedTrainingAccuracy[mistakes]))
    outFile.write ('% ')
    outFile.write (' testing Accuracy: ')
    outFile.write (str('%.2f' % myMC.averagedTestingAccuracy[mistakes]))
    outFile.write ('% \n')
'''
outFile.write ( 'testing Accuracy standard perceptron: ')
outFile.write (str('%.2f' % myMC.standardTrainingAccuracy[len(myMC.standardTrainingAccuracy) - 1]))
outFile.write ('% ')
outFile.write (' testing Accuracy averaged perceptron: ')
outFile.write (str('%.2f' % myMC.averagedTestingAccuracy[len(myMC.averagedTestingAccuracy) - 1]))
outFile.write ('% ')
outFile.write ('\n')

outFile.close()
