

lineList = []
vocabulary = {}

inFile = open ("CourseProject/train/train_medium2.csv", "r")

string = inFile.readline ()

while string:
    r_id = ''
    sentence = ''
    author = ''

    for character in range (1,8):
        r_id += string[character]
    for character in range (11,len(string) - 8):
        sentence += string[character]
    for character in range (len (string) - 5, len (string) - 2):
        author += string[character]

    lineList.append([r_id, sentence, author])

    string = inFile.readline ()

inFile.close()

word = ''
wordList = []
excludeDict = {' ':1, ',':1, '.':1, ';':1, ':':1, '"':1, '!':1, '?':1}

for line in lineList:
    for character in range (len(line[1])):
        if excludeDict.get (line[1][character], '--') != '--':
            word = str.lower(word)
            #wordList.append(word)
            if vocabulary.get(word, '--') == '--':
                vocabulary[word] = 1
            word = ''
        else:
            word += line[1][character]

wordList = vocabulary.keys()

for word in wordList:
    print word
