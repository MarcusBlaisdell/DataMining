########################
### Marcus Blaisdell
### Cpt_S 315
### Final project
### Spooky author identification
###
### Main.py
###
########################

from A_Class import *
from K_Class import *
from Functions import *

### Author Classifier
### create an instance of our class:
myAC = AClass()

'''
train_df = pd.read_csv("CourseProject/train/train.csv", usecols=[TEXT_COLUMN, Y_COLUMN])

unigram_pipe = Pipeline([('cv', CountVectorizer()),('mnb', MultinomialNB())])
test_pipeline(train_df, unigram_pipe, "Unigrams only")

#NLP = spacy.load('en', disable = ['parser', 'ner'])
logit_all_features_pipe = Pipeline([
    ('uni', UnigramPredictions()),
    ('nlp', PartOfSpeechFeatures()),
    ('clean', DropStringColumns()),
    ('clf', LogisticRegression())
                                 ])
test_pipeline(train_df, logit_all_features_pipe)

'''

### read data from text files:
### build stop list:
### get training data:
nounList = buildList ("CourseProject/POS/Nouns-mod.txt")
verbList = buildList ("CourseProject/POS/verbs-mod.txt")
adjectiveList = buildList ("CourseProject/POS/adjectives-mod.txt")
adverbList = buildList ("CourseProject/POS/adverbs-mod.txt")

myAC.readLines ("CourseProject/train/train.csv", myAC.trainData)
myAC.readLines ("CourseProject/train/test.csv", myAC.testData)
myAC.readStops ("CourseProject/train/stoplist.txt")
myAC.createWordList ()

myAC.initializeWeight ()
myAC.featureVectorList = buildFeatureList (myAC.vocabulary, myAC.trainData)
myAC.testVectorList = buildFeatureList (myAC.vocabulary, myAC.testData)
myAC.buildFrequencyWeights ()
myAC.perceptronFreq()

#myAC.perceptron()
myAC.buildFrequencyWeights ()

#for x in myAC.fwList:
    #print x
myAC.perceptronFreq()

myAC.frequencyPrediction ()
myAC.wordFrequency ()
#for tup in myAC.MWSfreq:
    #print tup

'''
printList = myAC.MWSfreq.keys()
for word in printList:
    print word + ' : ' + str (myAC.MWSfreq.get(word))
'''
#print myAC.wList[2][0]
#createARFF ("feature.arff", myAC.vocabulary, myAC.featureVectorList)
#createARFF ("feature.arff", myAC.vocabulary, myAC.frequencyList)

#for record in myAC.featureVectorList:
    #print record
#outFile.write ()

#for record in myAC.wordList:
    #print record
