'''
Marcus Blaisdell
CptS 315
Homework #2
2/28/18
Professor Jana Doppa

HW2_Functions.py

This file contains the functions called by HW2_Main.py
'''

from math import *


### read in ratings.csv into a matrix (list of lists)
### Determine the number of users from ratings.csv
####
def readRatings():

    inFile = open("ratings.csv", "r")

    string = inFile.readline()
    word = ""
    index = 0
    userIdMax = 0
    userList = []
    line = []

    while string:
        for x in string:
            if x == '\n':
                userList.append(line)
                line = []
                word = ""
            if x != ',':
                word += x
            else:
                if index == 0:
                    try:
                        word = int(word)
                        if word > userIdMax:
                            userIdMax = word
                    except:
                        pass

                line.append(word)

                index += 1

                word = ""
        index = 0

        string = inFile.readline()

    inFile.close()

    return userList
### end readRatings function

### read movies into list
def makeMovieList():
    inFile = open ("movies.csv", "r")

    movieList = {}
    line = []
    string = inFile.readline()
    word = ""

    while string:
        for x in string:
            if x == '\n':
                line.append(word)
                movieList[line[0]] = line[1]
                line = []
                word = ""
            elif x == ',':
                line.append(word)
                word = ""
            else:
                word += x

        string = inFile.readline()

    inFile.close()

    return movieList

### end makeMovieList function

    ### build an item (movies) matrix:

def readMovies(userList, userIdMax):
    inFile = open("movies.csv", "r")

    string = inFile.readline()
    word = ""
    index = 0
    movieDict = {}

    while string:
        for x in string:
            if x != ',' and x != '\n':
                word += x
            else:
                if index == 0:
                    if movieDict.get(word, 'n') == 'n':
                        #theList = [0] * (max(userDict.keys () ) + 1)
                        theList = [0] * (userIdMax + 1)
                        movieDict[word] = theList
                        #print word
                    else:
                        pass
                index += 1
                #print word
                word = ""
        index = 0
        string = inFile.readline()

    inFile.close()

    ### read through each line in the ratings matrix and add ratings to the
    ### item matrix in the appropriate locations
    ### userId's are indexes
    ### userList[0] = userId
    ### userList[1] = movieID
    ### userList[2] = ratings

    for x in userList:
        try:
            movieDict[x[1]][x[0]] = x[2]
        except:
            pass

    return movieDict

### end readMovies function

### calculate the centered-cosine similarity of two movies

def computeSim(movie_A, movie_B):
    ### normalize each list:

    ### val_A is a running sum of ratings
    ### divisor is a count of ratings
    val_A = 0.0
    divisor = 0.0

    ### check each rating, if it's greater than 0, add it to running ratings sum
    ### and increment ratings count

    for rating in movie_A:
        try:
            if rating != 0:
                val_A += float(rating)
                divisor += 1.0
        except:
            pass

    ### only adjust if there has been a rating

    if divisor > 0.0:
        ### the amount to offset is the average of the ratings:
        shift = val_A / divisor

        ### apply the offset to each rating, if there is more than one rating
        for ratingIndex in range(len(movie_A)):
            try:
                if movie_A[ratingIndex] > 0:
                    movie_A[ratingIndex] = float(movie_A[ratingIndex]) - shift
                    #print rating
            except:
                pass

    ### Repeat for the second movie:
    val_B = 0.0
    divisor = 0.0

    for rating in movie_B:
        try:
            if rating != 0:
                val_B += float(rating)
                divisor += 1.0
        except:
            pass

    if divisor > 0.0:
        shift = val_B / divisor

        for ratingIndex in range(len(movie_B)):
            try:
                if movie_B[ratingIndex] != 0:
                    movie_B[ratingIndex] = float(movie_B[ratingIndex]) - shift
                    #print rating
            except:
                pass

    ### The numerator is the sum of the products of the movies that each
    ### have a rating
    ### The denominator is the product of the roots of the sums of all ratings
    ### from each

    numerator = 0.0
    denominator = 0.0

    for x in range (len(movie_A) ):
        try:
            if movie_A[x] != 0.0 and movie_B[x] != 0.0:
                numerator += (movie_A[x] * movie_B[x])
        except:
            pass

    ### running sums for the squares of the ratings for each movie

    firstSum = 0.0
    secondSum = 0.0

    for x in range (len(movie_A) ):
        try:
            if movie_A[x] != 0.0:
                ### add the square of the ratings to the running sum
                firstSum += (movie_A[x] * movie_A[x])
        except:
            pass

    for x in range (len(movie_B) ):
        try:
            if movie_B[x] != 0:
                ### add the square of the ratings to the running sum
                secondSum += (movie_B[x] * movie_B[x])
        except:
            pass

    score = 0.0

    firstRoot = 0.0
    secondRoot = 0.0

    if numerator != 0:
        firstRoot = sqrt(firstSum)
        secondRoot = sqrt(secondSum)
        denominator = firstRoot * secondRoot

        score = numerator / denominator

    return score

### end computeSim function

### This will take ~3 hours!!!

def scoreMovies(movieDict):
    ### formatting:
    #{movie_A:[[[(A,B), score], [(A,B), score],[(A,B), score],[(A,B), score],[(A,B), score]] }
    #{movie_B:[[[(A,B), score], [(A,B), score],[(A,B), score],[(A,B), score],[(A,B), score]] }
    scoreList = {}
    movieList = movieDict.keys()
    theScore = 0.0
    for x in range (len(movieList)): ### this is the real line
    #for x in range (1000): ### shorter list for testing
        #for y in range (x + 1, 100): ### shorter list for testing
        for y in range (x + 1, len(movieList)): ### this is the real line
            pair = (movieList[x], movieList[y])
            theScore = computeSim (movieDict.get(movieList[x]), movieDict.get(movieList[y]))

            if theScore > 0:
                if scoreList.get(movieList[x], 'n') == 'n':
                    scoreList[movieList[x]] = [[(0,0),0],[(0,0),0],[(0,0),0],[(0,0),0],[(0,0),0]]
                if scoreList.get(movieList[y], 'n') == 'n':
                    scoreList[movieList[y]] = [[(0,0),0],[(0,0),0],[(0,0),0],[(0,0),0],[(0,0),0]]

                tempList_A = scoreList.get(movieList[x])

                for z in range (5):
                    if theScore > tempList_A[z][1]:
                        tempPair = tempList_A[z][0]
                        tempVal = tempList_A[z][1]
                        tempList_A[z][0] = pair
                        tempList_A[z][1] = theScore
                        pair = tempPair
                        theScore = tempVal

                scoreList[movieList[x]] = tempList_A

                tempList_B = scoreList.get(movieList[y])
                for z in range (5):
                    if theScore > tempList_B[z][1]:
                        tempPair = tempList_B[z][0]
                        tempVal = tempList_B[z][1]
                        tempList_B[z][0] = pair
                        tempList_B[z][1] = theScore
                        pair = tempPair
                        theScore = tempVal
                scoreList[movieList[y]] = tempList_B

    return scoreList

### end scoreMovies function

### For testing, so I don't have to re-run the time-consuming
### calculations, I can read them from file

def readScoresFromFile():
    ### read in from file to dictionary

    inFile = open ("output.txt", "r")
    string = inFile.readline

    line = []
    word = ""
    testDict = {}

    while string:
        for x in string:
            if x == '\n':
                line.append(word)
                word = ""
                storeList = []
                line1 = line[1]
                line2 = line[2]
                pair1 = (line1, line2)
                score1 = line[3]
                pair2 = (line[4], line[5])
                score2 = line[6]
                pair3 = (line[7], line[8])
                score3 = line[9]
                pair4 = (line[10], line[11])
                score4 = line[12]
                pair5 = (line[13], line[14])
                score5 = line[15]
                list1 = [pair1, score1]
                list2 = [pair2, score2]
                list3 = [pair3, score3]
                list4 = [pair4, score4]
                list5 = [pair5, score5]
                storeList = [list1, list2, list3, list4, list5]
                testDict[line[0]] = storeList
                line = []

            elif x == ',':
                line.append(word)
                word = ""
            elif x != '(' and x != ')' and x!= '[' and x!= ']' and x!= ' ':
                word += str(x)
            else:
                pass

        string = inFile.readline()
    inFile.close()

    return testDict
### end readScoresFromFile function


### estimate the ratings for any unrated movie for each user,
### maintain a running list of the top 5 for recommendations

def estimateRatings(userList, scoreList, movieDict, maxUserId):
    movieList = movieDict.keys()
    userRecommendations = {}
    userRecommendationsList = []

    for movie in movieList:
        ratingList = movieDict.get(movie)

        for user in range (1, maxUserId + 1):
            if ratingList[user] == 0:
                neighborhood = scoreList.get(movie)
                rating = 0.0
                divisor = 0.0
                pair = (0,0)
                ### estimate the users rating for this movie
                try:
                    for x in neighborhood:
                        movie_2 = x[0][1]
                        if movieDict.get(movie_2)[user] > 0:
                            rating += movieDict.get(movie_2)[user] * x[1]
                            divisor += x[1]

                    userRating = rating / divisor

                    ### if there is already a dictionary entry for this user,
                    ### get it's list of top recommendations
                    ### to be updated with new information

                    if userRecommendations.get(user, 'n') != 'n':

                        userRecommendationsList = userRecommendations.get(user)
                    ### if there is not a dictionary entry for this user,
                    ### add one, and then get it's empty list to start
                    ### populating
                    else:
                        userRecommendations[user] = [[0,0.0], [0,0.0], [0,0.0], [0,0.0], [0,0.0]]
                        userRecommendationsList = userRecommendations.get(user)
                    ### keep only the top 5
                    userMovie = movie_2
                    for y in range(5):
                        if userRating > userRecommendationsList[y][1]:
                            tempRating = userRecommendationsList[y][1]
                            tempMovie = userRecommendationsList[y][0]
                            userRecommendationsList[y][1] = userRating
                            userRecommendationsList[y][0] = userMovie
                            userRating = tempRating
                            userMovie = tempMovie
                    userRecommendations[user] = userRecommendationsList
                except:
                    pass

    return userRecommendations


### end estimateRatings function

### print recommendations to a file

def printRecommendations(userDict, movieList):
    outFile = open ("movieRecommendations.txt", "w")

    for user in userDict.keys():
        for movie in userDict.get(user):
            if movieList.get(movie[0], 'n') != 'n':
                outFile.write(str(user))
                outFile.write (' you may enjoy: ')
                outFile.write (str(movieList.get(movie[0])))
                outFile.write ('\n')

    outFile.close()

### end printRecommendations function

def printOutput(userDict):
    outFile = open ("output.txt", "w")
    for x in userDict.keys():
        outFile.write ('User-id')
        outFile.write (str(x))
        outFile.write (' ')
        for y in range (5):
            outFile.write ('movie-id')
            outFile.write (str(userDict.get(x)[y][0]))
            outFile.write (' ')
        outFile.write ('\n')
    outFile.close ()

### end printOutput function
