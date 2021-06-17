'''
Marcus Blaisdell
CptS 315
Homework #2
2/28/18
Professor Jana Doppa

HW2_Main.py

This file is the main program
'''

###
import json
from HW2_Functions import *
from math import *

movieDict = {}
scores = {}
score = 0.0
userList = []
pairList = []
maxUserId = 671

userList = readRatings()
movieDict = readMovies(userList, userList[len(userList) - 1][0])
movieList = makeMovieList()

### uncomment this block to read scores from file instead of
### re-calculating
'''
### read scoreList from file
scoreList = {}
scoreList = readScoresFromFile()
print scoreList
### end read scoreList from file
'''

scoreList = {}
scoreList = scoreMovies(movieDict)

### calculate recommendations
userDict = estimateRatings(userList, scoreList, movieDict, userList[len(userList) - 1][0])

### print recommendations to a nicely formatted text file:
printRecommendations(userDict, movieList)

### save results to text files:

printOutput(userDict)

### print *Done* message to user:

print ' '
print '*** Complete ***'
print ' '
