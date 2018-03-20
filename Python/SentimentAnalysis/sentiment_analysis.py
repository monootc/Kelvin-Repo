'''
COMP 151 Artificial Intelligence, Fall 2017
Professor Chadi
Project 3: Sentiment Analysis
Description: Using Bays Algorithm, categorize the movie reviews into fresh or  rotten.
'''

import string
from collections import Counter
from configuration import *


class SentimentAnalysis():
    def __init__(self, good_review_file, bad_review_file):
        good_lines = self.readFile(good_review_file)
        bad_lines = self.readFile(bad_review_file)
        good_reviews = self.removePunctuation(good_lines)
        bad_reviews = self.removePunctuation(bad_lines)
        self.rotten_prob = 1.0
        self.fresh_prob = 1.0
        self.num_of_good_review = len(good_reviews)
        self.num_of_bad_review = len(bad_reviews)
        good_word_list = self.removeWords(good_reviews)
        bad_word_list = self.removeWords(bad_reviews)
        self.prob_of_good_review = self.num_of_good_review / (self.num_of_good_review + self.num_of_bad_review)
        self.prob_of_bad_review = self.num_of_bad_review / (self.num_of_good_review + self.num_of_bad_review)
        self.good_wordCount = len(good_word_list)
        self.bad_wordCount = len(bad_word_list)
        self.bad_word_dict = Counter(bad_word_list)
        self.good_word_dict = Counter(good_word_list)
        self.getConditionalProb()


    # input: None
    # output: None
    # description: calculate the conditional probability for fresh and rotten reviews
    def getConditionalProb(self):
        for k, v in self.good_word_dict.items():
            self.good_word_dict[k] = v / self.good_wordCount
        for k, v in self.bad_word_dict.items():
            self.bad_word_dict[k] = v / self.bad_wordCount

    # input: test file name
    # output: rotten or fresh
    # description: perform Baysian test by multiplying the prob. of each word in the test file with fresh and rotten
    #              prob. Return fresh if fresh prob. is higher than rotten and vice versa
    def baysianTest(self, test_file):
        test_lines = self.readFile(test_file)
        test_review = self.removePunctuation(test_lines)
        test_word_list = self.removeWords(test_review)
        fresh_scores = []
        rotten_scores = []
        for word in test_word_list:
            if word in self.good_word_dict.keys():
                fresh_scores.append(self.good_word_dict[word])
            else:
                fresh_scores.append(LOW_PROB)

        for word in test_word_list:
            if word in self.bad_word_dict.keys():
                rotten_scores.append(self.bad_word_dict[word])
            else:
                rotten_scores.append(LOW_PROB)

        for data in fresh_scores:
            self.fresh_prob = self.fresh_prob * data * MAGNIFYING_CONST

        for data in rotten_scores:
            self.rotten_prob = self.rotten_prob * data * MAGNIFYING_CONST
        verdict = "fresh" if self.fresh_prob > self.rotten_prob else "rotten"
        return verdict


    # input: file name
    # output: lines of the file
    # description: read lines, handle exception
    def readFile(self, filename):
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
            return lines
        except IOError as e:
            print("I/O error({}): {}".format(e.errno, e.strerror))


    # input: lines of the file
    # output: list of lists of reviews
    # description: remove punctuations, return the reviews in the lists of list format
    def removePunctuation(self, lines):
        translator = str.maketrans('', '', string.punctuation)
        all_reviews = [line.translate(translator).split() for line in lines]
        return all_reviews


    # input: reviews
    # output: list of words
    # description: make all words lowercase and remove common words
    def removeWords(self, reviews):
        word_list = [j.lower() for i in reviews for j in i if j not in REMOVE_WORDS]
        return word_list


    # input: None
    # output: None
    # description: print stats
    def printStat(self):
        print("Number of fresh reviews in the training file:       {}".format(self.num_of_good_review))
        print("Number of words in the fresh review training file:  {}".format(self.good_wordCount))
        print("Probability of a fresh review:                      {}\n".format(self.prob_of_good_review))
        print("Number of rotten reviews in the training file:      {}".format(self.num_of_bad_review))
        print("Number of words in the rotten review training file: {}".format(self.bad_wordCount))
        print("Probability of a rotten review:                     {}\n".format(self.prob_of_bad_review))


    # input: test file
    # output: None
    # description: print result, fresh or rotten
    def printResult(self, test_file):
        print("Now analyzing {}".format(test_file))
        result = self.baysianTest(test_file)
        file_name = test_file.split('\\')[-1] if '\\' in test_file else test_file
        print("The score as a fresh review:     {}".format(self.fresh_prob))
        print("The score as a rotten review:    {}".format(self.rotten_prob))
        print("Verdict:                         {} is a {} review!\n".format(file_name, result))


    # optional input: display, outputFile
    # output: output file if outFile option is on
    # description: dumb the content of the words map, either display and/or save in a file
    def dumpContentOfMap(self, display = False, outFile = None):
        if outFile is not None:
            with open(outFile, 'w') as f:
                for k, v in self.good_word_dict.items():
                    f.write(k + ": " + str(v) + '\t')
                for k, v in self.bad_word_dict.items():
                    f.write(k + ": " + str(v) + '\t')
            f.close()

        if display is True:
            print(self.good_word_dict)
            print(self.bad_word_dict)


def main():
    s = SentimentAnalysis(GOOD_REVIEW_TRAINING, BAD_REVIEW_TRAINING)
    s.printStat()
    s.dumpContentOfMap(DISPLAY, OUTFILE)
    if SELF_TEST_MODE is True:
        for i in range(1,9):
            test_file = TEST_FILE_PATH + 'test' + str(i) + '.txt'
            s.printResult(test_file)
    else:
        try:
            s.printResult(TEST_OWN_FILE)
        except IOError as e:
            print("I/O error({}): {}".format(e.errno, e.strerror))

if __name__=="__main__":
    main()