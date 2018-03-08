'''
Project 1:      Genetic Algorithm
Description:    An algorithm that mimics the genetic evolution, producing next generations from selection and cross methods
                users can define the following:
                    * # of initial chromosomes
                    * # of chromosomes in each generation
                    * # of generations
                    * selection type: tournament or elitist
                    * crossover type: uniform or kpoint
                    * mutation type: varied or fixed
                    * mutation rate: between 1 to 100
                    * mutation rate change per generation: between 1 to 100
Author:         Kelvin Hu
Date:           9/26/17
'''

import numpy
import random
import time
import math
from config import *
import sys


# global variable to store the data read from the data.txt file
data = []


# input: None
# Output: selection function and cross function
# Description: Validate inputs from the config file. And return the corresponding selection func and cross func
def checkConfig():
    if SELECTION_TYPE == 'tournament':
        selectFuncToCall = tournament
    elif SELECTION_TYPE == 'elitist':
        selectFuncToCall = elitist
    else:
        raise ValueError('Selection type is not valid!')

    if CROSS_TYPE == 'uniform':
        crossFuncToCall = uniform
    elif CROSS_TYPE == 'kpoint':
        crossFuncToCall = kPoint
    else:
        raise ValueError('Cross type is not valid!')

    if NUM_OF_GENERATIONS<0 or NUM_OF_CHROM_PER_GEN < 0 or NUM_OF_INITIAL_CHROM < 0:
        raise ValueError("Number must be bigger than 0")

    if 0 > PERCENTAGE_OF_SELECTION or PERCENTAGE_OF_SELECTION > 1:
        raise ValueError("Percentage of selection must be between 0 to 1")

    if MUTATION_RATE > 100 or MUTATION_RATE < 0:
        raise ValueError("Mutation rate must be between 0 to 100")

    if MUTATION_RATE_CHANGE_PER_GEN > 100 or MUTATION_RATE_CHANGE_PER_GEN < 0 or MUTATION_RATE_CHANGE_PER_GEN > MUTATION_RATE:
        raise ValueError("Mutation rate change per generation between be between 0 to 100 and less than mutation rate")

    if MUTATION_TYPE != 'varied' and MUTATION_TYPE != 'fixed':
        raise ValueError("Mutation type must be either varied or fixed")
    return crossFuncToCall, selectFuncToCall


# input: None
# output: parameters to run this program
def displaySetting():
    retStr = """
    Setting for this run:
    Data file = {}
    Initial Population = {}
    Number of Chromosome per generation = {}
    Number of generations = {}
    Crossover type = {}
    Percentage of selection = {}
    Selection type = {}
    Mutation type= {}
    Mutation rate = {}
    Mutation rate change per generation = {}

        """.format(str(DATA_FILE), NUM_OF_INITIAL_CHROM, NUM_OF_CHROM_PER_GEN, NUM_OF_GENERATIONS, CROSS_TYPE,
                   PERCENTAGE_OF_SELECTION, SELECTION_TYPE, MUTATION_TYPE, MUTATION_RATE, MUTATION_RATE_CHANGE_PER_GEN)
    return retStr


# decoration function
def decorator_func(func):
    def wrapper_func(*args, **kwargs):
        print("Running {} now... be patient!".format(func.__name__))
        result = func(*args,**kwargs)
        print("\nFinally Done!")
        return result
    return wrapper_func


# input: None
# output: a random number with 0 mean and 1.15 standard deviation
def getRandom():
    return(numpy.random.normal(0, 1.15))


# input: list of generation
# output: None
# description: print out a generation class, for debugging purpose to verify the data is correct
def debug(generations):
    for eachGen in generations:
        for gen in eachGen:
            print(gen)

# input: a list of values
# output: a ordered list [a, b, c, d] such that b > a, and c > d
# description: this order needs to be maintained for all the genes in Chromosome class
def orderValues(values):
    if values[0] > values[1]:
        values[1], values[0] = values[0], values[1]
    if values[2] > values[3]:
        values[3], values[2] = values[2], values[3]


# input: None
# output: fill the global data with the contents of the file
def readFile():
    global data
    try:
        with open(DATA_FILE, 'r') as f:
            for item in f.readlines():
                item = item.strip()
                data.append(item.split('\t'))
    except:
        raise ValueError("Error: Can't open the file")


# input: a list of chromosome class
# output: a list of chromosome class
# description: sort the input chromosomes, and return the user defined number of top chromosomes
def elitist(chromosomes):
    chromosomes = sorted(chromosomes)
    elitChrm = chromosomes[:math.floor(PERCENTAGE_OF_SELECTION * NUM_OF_CHROM_PER_GEN)]
    return elitChrm


# input: a list of chromosome class
# output: a list of chromosome class
# description: chromosomes are randomly chosen (1 chromo can be chosen multiple times) and compare the score, the one with
#              higher score are appended in the winners and returned
def tournament(chromosomes):
    winners = []
    length = len(chromosomes)
    for i in range(math.floor(NUM_OF_CHROM_PER_GEN * PERCENTAGE_OF_SELECTION)):
        fPos = random.randint(0, length-1)
        sPos = random.randint(0, length-1)
        if chromosomes[fPos] > chromosomes[sPos]:
            winners.append(chromosomes[fPos])
        else:
            winners.append(chromosomes[sPos])
    return winners


# input: a list of chromosome class
# output: a list chromosome class
# description: generate new Chromosomes using k-point method, the number of chrom is the Chromo per generation - the percentage
#              for selection
def kPoint(chrm):
    newGene = []
    newChrom= []
    l = len(chrm)
    for i in range(NUM_OF_CHROM_PER_GEN-math.floor(PERCENTAGE_OF_SELECTION*NUM_OF_CHROM_PER_GEN)):
        fPos = random.randint(0, l-1)
        sPos = random.randint(0, l-1)
        newGene = (chrm[fPos].gene[:2] + chrm[sPos].gene[2:])
        newChrom.append(Chromosome(newGene))
    return newChrom


# input: a list of chromosome class
# output: a list of chromosome class
# description: generate new Chromosomes using uniform method, the number of chrom is the Chromo per generation - the percentage
#              for selection
def uniform(chrm):
    newChrom = []
    length = len(chrm)
    for i in range(NUM_OF_CHROM_PER_GEN-math.floor(PERCENTAGE_OF_SELECTION*NUM_OF_CHROM_PER_GEN)):
        temp = []
        fPos = random.randint(0, length-1)
        sPos = random.randint(0, length-1)
        for j in range(5):
            parent = random.randint(0, 1)
            if parent == 0:
                temp.append(chrm[fPos].gene[j])
            else:
                temp.append(chrm[sPos].gene[j])
        orderValues(temp)
        newChrom.append(Chromosome(temp))
    return newChrom


# input: mutation rate ( 1 to 100 )
# output: mutation rate ( 1 to 100 )
# description: if Mutation type is fixed, then just return mutation rate unchanged,
#              otherwise, return mutation rate - change per generation
def setMRate(mRate):
    if MUTATION_TYPE == 'fixed':
        return MUTATION_RATE
    else:
        if mRate > 1:
            return(mRate-MUTATION_RATE_CHANGE_PER_GEN)
        else:
            return 1


# input: orginal Chromosomes, selection function, cross type function
# output: a list of generations
# description: main function to generate generations, the list is grouped in 10 for easier stats calculatioin
@decorator_func
def makeGenerations(origGen, selectionFunc, typeFunc):
    newPopulation = []
    mutationRate = setMRate(MUTATION_RATE)
    if NUM_OF_GENERATIONS > 1:
        for i in range(NUM_OF_GENERATIONS):
            sys.stdout.write("\r%d%%" % ((i/NUM_OF_GENERATIONS)*100))
            sys.stdout.flush()
            origGen = selectionFunc(origGen)
            origGen += typeFunc(origGen)
            for j in range(len(origGen)):
                origGen[j].mutation(mutationRate)
                origGen[j].calculateScore()
            newGen = Generation(origGen, i+1)
            mutationRate = setMRate(mutationRate)
            newPopulation.append(newGen)
    newPopulation = [newPopulation[x:x+10] for x in range(0, len(newPopulation), 10)]
    for generations in newPopulation:
        for eachGen in generations:
            eachGen.gen = sorted(eachGen.gen, reverse=True)
    return newPopulation


# input: a list of generation
# output: a list of average score, a list chromo class that has max scores, a list chromo class that has min scores
@decorator_func
def getStats(population):
    allScores=[]
    maxChroms=[]
    minChroms = []
    maxC = []
    maxScore = 0
    minScore = 10000
    minC = []
    for generations in population:
        for eachGen in generations:
            maxChroms.append(eachGen.gen[0])
            minChroms.append(eachGen.gen[-1])
            for i in range(NUM_OF_CHROM_PER_GEN):
                allScores.append(eachGen.gen[i].score)

    avgScores = [avg for avg in [(sum(allScores[i:i+NUM_OF_CHROM_PER_GEN*10])/(NUM_OF_CHROM_PER_GEN*10))
                                 for i in range(0, len(allScores), (NUM_OF_CHROM_PER_GEN*10))]]
    for i in range(0, len(minChroms), 10):
        for chroms in minChroms[i:i+10]:
            if chroms.score < minScore:
                minScore = chroms.score
                minChrom = chroms
        minC.append(minChrom)
        minScore = 10000

    for i in range(0, len(maxChroms), 10):
        for chroms in maxChroms[i:i+10]:
            if chroms.score > maxScore:
                maxScore = chroms.score
                maxChrom = chroms
        maxC.append(maxChrom)
        maxScore = 0
    return avgScores, maxC, minC


# input: a list of max generations class
# output: None
# description: create a csv file in the same directory as the script that contains all the data
def writeToCsv(maxGens):
    timestamp = time.strftime('%H%M')
    filename = timestamp + "_project1_results.csv"
    with open(filename, 'w') as csvfile:
        csvfile.write(displaySetting())
        for gen in maxGens:
            csvfile.write(str(gen))


# input: a list of generation class
# output: None
# description: displays the average, max and min for each 10 generations
def display(avg, theMax, theMin, generations):
    l = len(theMin)
    print(displaySetting())
    for i in range(l):
        lower = i*10+1
        upper = (i+1)*10
        if upper > NUM_OF_GENERATIONS:
            upper = NUM_OF_GENERATIONS
        print("Stats for generations {:3d} to {:3d}:".format(lower, upper))
        print("Average is \033[95m{:.2f}\033[0m".format(avg[i]))
        print("Maxinum Chromosome is \033[94m{}\33[0m, score is \33[94m{:.2f}\033[0m".format(theMax[i].gene, theMax[i].score))
        print("Minimum Chromosome is \033[92m{}\33[0m, score is \33[92m{:.2f}\033[0m".format(theMin[i].gene, theMin[i].score))
    print("\nThe maxinum chromosome in the last generation is \033[91m{}\33[0m, score is \033[91m{:.2f}\33[0m".format(generations[-1][0].gen[0].gene,
                                                                                          generations[-1][0].gen[0].score))

class Chromosome:
    def __init__(self, ch = None):
        self.score = 0
        if ch is None:
            self.gene = []
            for i in range(4):
                self.gene.append(getRandom())
            orderValues(self.gene)
            self.gene.append(random.randint(0,1))
        else:
            self.gene = ch


    def calculateScore(self):
        totalScore = 0
        found = False
        for item in data:
            if (self.gene[0] <= float(item[0]) <= self.gene[1]) and \
                    (self.gene[2] <= float(item[1]) <= self.gene[3]):
                found = True
                if (self.gene[-1] == 1):
                    totalScore = totalScore + float(item[-1])
                else:
                    totalScore = totalScore + float(item[-1]) * -1
        if found == False:
            self.score = -5000
        else:
            self.score = totalScore

    def mutation(self, mRate):
        for i in range(len(self.gene)):
            chance = random.randint(1, 100)
            if chance<mRate:
                if i == 4:
                    self.gene[i] = random.randint(0, 1)
                else:
                    self.gene[i] = getRandom()
        orderValues(self.gene)

    def __gt__(self, other):
        return(self.score > other.score)

    def __str__(self):
        return(str(self.gene)[1:-1] + ',' + str(self.score)) + '\n'

class Generation:
    def __init__(self, chromList, index):
        self.genIndex = index
        self.gen = chromList

    def __str__(self):
        retStr = "Generation " + str(self.genIndex) + '\n'
        for i in range(len(self.gen)):
            for j in range(5):
                retStr += str(self.gen[i].gene[j]) + '  '
            retStr += 'score: ' + str(self.gen[i].score) + '\n'
        return retStr


def main():
    cFuncToCall, sFuncToCall = checkConfig()
    readFile()
    chromosomes = []
    for i in range(NUM_OF_INITIAL_CHROM):
        chromosomes.append(Chromosome())
        chromosomes[i].calculateScore()
    gens = makeGenerations(chromosomes, sFuncToCall, cFuncToCall)
    avg, maxGens, minGens = getStats(gens)
    display(avg, maxGens, minGens, gens)
    writeToCsv(maxGens)
    # uncommon debug if u want to see the output for every generation
    #debug(gens)
if __name__ == '__main__':
    main()