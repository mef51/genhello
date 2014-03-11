#!/usr/bin/python

import random
import utils

###
# This function assesses how similar two strings are.
# Assigns a distance metric to `string` as compared to `target`.
# If string == target, then stringScore(string) == 0.
# That is, the perfect string is the string that matches target
# The higher the distance, the further away the string is from the target
#
# Distance is calculated based on the following
# * length of the string --> the closer they are in length the better
# * common chars --> if a character is present in both, good, otherwise, bad
# * character frequency --> count the common chars, if they appear the same # of times, good, else, bad
#
# The actual formulas for calculating a score based on those traits is pretty arbitrary, except for the
# restriction that the score is 0 if the string and target are the same.
# Based on how big of a number you return you could be weighting the different traits as more important than
# others. Which makes you ask, what's the best way to weight the different traits? Could
# use an optimization algorithm to optimize your optimization algorithm?!?!
def stringDistance(string, target="hello, world!"):
    distance = 0
    print "*********************************"
    print "Assessing String: " + string

    # ignore case for now
    string = string.lower()
    target = target.lower()

    # Length. The bigger the difference in length, the worse.
    lengthDistance = utils.lengthsDifference(string, target)

    # Common Chars
    comCharsDistance = utils.compareCommonChars(string, target)

    # Char Frequency
    frequencyDistance = utils.compareFrequency(string, target)

    # Char Order
    orderDistance = utils.compareCharacterOrder(string, target)

    # Weight Factors to control importance. Can these be optimized?
    lengthFactor    = 1.0
    comCharFactor   = 1.0
    frequencyFactor = 1.0
    orderFactor     = 1.0

    distance += lengthDistance    * lengthFactor
    distance += comCharsDistance  * comCharFactor
    distance += frequencyDistance * frequencyFactor
    distance += orderDistance     * orderFactor
    print "Length Score: "      + `lengthDistance`
    print "Commonality Score: " + `comCharsDistance`
    print "Frequency Score: "   + `frequencyDistance`
    print "Order Score: "       + `orderDistance`
    print "Total Score: "       + `distance`

    return distance

# adapted from toby seragan's book "Programming Collective Intelligence"
# By default, loops forever until the "perfect solution" is found:
# until the costFun returns 0 for a member of the population.
# Set maxIterations to a number greater than 0 to control when to stop.
def geneticOptimize(alphabet, costFun, popSize = 100, mutProb = 0.2, eliteProp = 0.2, maxIterations = 0):
    topElite = int(eliteProp * popSize) # Number of members that survive to the next generation

    population = []
    for i in range(popSize):
        population.append(utils.getRandomString()) # Initial population

    numGenerations = 0

    # Mutation operation.
    # Replace the i-th index with a random char and return the result. Don't change `vector`
    def mutate(vector):
        i = random.randint(0, max(0, len(vector) - 1))
        return vector[0:i] + utils.getRandomChar() + vector[i+1:]

    # Crossover operation. Take one part from r1 and another part from r2 and stick em together
    def crossover(r1, r2):
        def randIndex(v): # get a random index for v, but never 0
            return random.randint(1, max(1, len(v) - 1))

        # using i and j will change the length of the result
        i = randIndex(r1)
        j = randIndex(r2)

        # using k makes the length of the result = length of the longer string, always
        k = min(i, j)

        # We want the length to mutate occasionally (especially at the beginning)
        # but not all the time, since it can be destructive. So we'll let the length change only half the time
        if random.random() < 0.5:
            return r1[0:i] + r2[j:]
        else:
            return r1[0:k] + r2[k:]

    # Main loop
    while True:
        # an iteration of learning. Returns the best scored member of the population at the end
        scores = [(costFun(v), v) for v in population]
        scores.sort() # lowest scores first.
        ranked = [v for v in scores]

        # kill the weak
        population = []
        for v in ranked[0 : topElite]: # lower scores are better
            population.append(v[1])

        # Add mutated and bred forms to fill the remaining population
        while len(population) < popSize:
            if random.random() < mutProb:
                # mutate
                c = random.randint(0, len(ranked) - 1) # pick a random survivor
                population.append(mutate(ranked[c][1])) # mutate the random survivor and add to the population
            else:
                # crossover two random surivors
                c1 = random.randint(0, topElite)
                c2 = random.randint(0, topElite)
                population.append(crossover(ranked[c1][1], ranked[c2][1]))

        # print `numGenerations` + ': ' + scores[0][1] # print most fit in generation

        mostFit = scores[0]
        numGenerations += 1
        # if the mostFit got a perfect score, quit
        if mostFit[0] == 0 or (maxIterations > 0 and numGenerations == maxIterations):
            print "Finished, Generations: " + `numGenerations`
            return mostFit

# geneticOptimize(utils.alphabet, stringDistance, popSize = 100, maxIterations = 20)

stringDistance('he')
stringDistance('hel')
