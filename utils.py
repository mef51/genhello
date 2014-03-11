import math
import random

alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890,.?!@#$%^&*- ()'

# Returns the difference in lengths
def lengthsDifference(a, b):
    return math.fabs(len(a) - len(b))

# Compares the common characters in a and b and returns the score of a compared to b
# The bigger the number the less similar they are. 0 Means they are the same
# TODO: Need to penalize if there are missing chars, chars that *should* be common but aren't
def compareCommonChars(wordA, wordB):
    result = 0.0
    numUniqueInWordA = len(getUniqueElements(wordA))
    numUniqueInWordB = len(getUniqueElements(wordB))
    commonUniqueChars = getCommonUniqueChars(wordA, wordB)
    numUncommon = numUniqueInWordA - len(commonUniqueChars)

    # The proportion of wordA that holds chars that are incorrect
    result += float(numUncommon) / numUniqueInWordA

    # The proportion of unique chars that wordA is missing from wordB
    result += 1 - float(numUniqueInWordA) / numUniqueInWordB
    return result * 100

# Returns the sum of the differences in occurrences of characters common to both words
# Ex. compareFrequency of "goodbye" and "hello"
# The common chars are 'o' and 'e'.
# 'o' happens 2 times in 'goodbye' and 1 time in 'hello'. 2 - 1 = 1
# 'e' happens 1 time  in 'goodbye' and 1 time in 'hello'. 1 - 1 = 0
# So return 1 + 0 = 1.
def compareFrequency(wordA, wordB):
    commonUniqueChars = getCommonUniqueChars(wordA, wordB)
    result = 0
    for char in commonUniqueChars:
        result += math.fabs(wordA.count(char) - wordB.count(char))
    return result

def getUniqueElements(word):
    uniqueChars = []
    for char in word:
        if uniqueChars.count(char) == 0:
            uniqueChars.append(char)
    return uniqueChars

def compareCharacterOrder(wordA, wordB):
    commonUniqueChars = getCommonUniqueChars(wordA, wordB)
    distance = 0
    for char in commonUniqueChars:
        copyA = wordA
        copyB = wordB
        while copyA.find(char) > -1 and copyB.find(char) > -1:
            aPos = copyA.find(char)
            bPos = copyB.find(char)
            distance += math.fabs(aPos - bPos)
            copyA = copyA[aPos + 1: len(copyA)]
            copyB = copyB[bPos + 1: len(copyB)]
    return distance

# Returns the union of two lists composed of unique elements (no duplicates allowed)
def union(listA, listB):
    result = []
    for elem in listA:
        if listB.count(elem) > 0:
            result.append(elem)
    return result

def getCommonUniqueChars(wordA, wordB):
    uniqueA = getUniqueElements(wordA)
    uniqueB = getUniqueElements(wordB)
    return union(uniqueA, uniqueB)

def getRandomString(maxLength = 50):
    length = random.randint(1, maxLength)
    s = ''
    for i in range(length):
        s += getRandomChar()
    return s

def getRandomChar():
    return random.choice(alphabet)

def demoHowSlowRandomnessIs():
    count = 0
    while 1:
        s = getRandomString()
        count += 1
        if count % 10000 == 0:
            print `count` + ": " + getRandomString()

        if s == "hello, world!":
            print `count` + ": " + getRandomString()
            break
