'''
COMP 151 Artificial Intelligence, fall 2017
Professor:      Chadi
Project 2:      Perceptron
Description:    Single layer perceptron, identify the location with a given pair of latitude and longtitude
'''

from configuration import *
import random


# Description: parse the file
# input: file name
# output: data list
def readFile(file_name):
    data = []
    with open(file_name, 'r') as f:
        file = f.readlines()
        for item in file:
            item = item.strip()
            data.append(item.split('\t'))
    return data



class Perceptron():
    _learning_rate = LEARNING_RATE
    _treshold = THRESHOLD
    _n_epoch = N_EPOCH
    _bias = BIAS
    def __init__(self, location, weight1 = WEIGHT_1, weight2 = WEIGHT_2, bias_weight = BIAS_WEIGHT):
        self.location = location
        if weight1 == None and weight2 == None and bias_weight == None:
            self.weights = [random.randint(0,10), random.randint(0, 10), random.randint(0, 10)]
        else:
            self.weights = [weight1, weight2, bias_weight]
        self.true_positive = 0
        self.true_negative = 0
        self.false_positive = 0
        self.false_negative = 0
        self.correct = 0
        self.incorrect = 0


    # Description: activation function
    # input: each row of the training data
    # output: 1 if it's greater than the threshold, 0 otherwise
    def predict(self, row):
        activate = 0
        for i in range(len(row)-1):
            activate += self.weights[i] * float(row[i]) + self.weights[2] * self._bias
        if activate >= self._treshold:
            return 1
        else:
            return 0


    # Description: update the weights using the training data
    # input: training data
    # output: updated weights
    def train_weights(self, data):
        for epoch in range(self._n_epoch):
            for row in data:
                prediction = self.predict(row)
                expected = self.getExpectation(row[-1])
                sum_error = expected - prediction
                for i in range(len(self.weights)-1):
                    self.weights[i] = self.weights[i] + self._learning_rate * sum_error * float(row[i])
                self.weights[2] = self.weights[2] + sum_error * self._bias

    # Description: get the expected value from the last column of the training data
    # input: last column of the training data
    # output: 1 if matched, 0 otherwise
    def getExpectation(self, loc):
        if (loc == self.location):
            return 1
        else:
            return 0


    # Description: test function
    # input: test data
    # output: update the statistics
    def test(self, data):
        for row in data:
            prediction = self.predict(row)
            expected = self.getExpectation(row[-1])
            if prediction == expected == 1:
                self.correct += 1
                self.true_positive += 1
            elif prediction == expected == 0:
                self.correct += 1
                self.true_negative += 1
            elif prediction == 1 and expected == 0:
                self.incorrect += 1
                self.false_positive += 1
            elif prediction == 0 and expected == 1:
                self.incorrect += 1
                self.false_negative += 1


    # Description: print the percentage statistics
    # input: none
    # output: none
    def printStats(self):
        total = self.incorrect + self.correct
        true_pos_per = self.getPercentage(self.true_positive, total)
        true_neg_per = self.getPercentage(self.true_negative, total)
        false_pos_per = self.getPercentage(self.false_positive, total)
        false_neg_per = self.getPercentage(self.false_negative, total)
        correct_per = self.getPercentage(self.correct, total)
        incorrect_per = self.getPercentage(self.incorrect, total)
        print('''
            Neuron: {}
                Correct: {}%
                    True Positive: {}%
                    True Negative: {}%
                Incorrect: {}%
                    False Positive: {}%
                    False Negative: {}%
            '''.format(self.location, correct_per, true_pos_per, true_neg_per, incorrect_per, false_pos_per, false_neg_per)
            )

    def getPercentage(self, attr, total):
        return round((attr / total * 100) ,2)


def main():
    training_data = readFile(TRAINING_FILE)
    testing_data = readFile(TEST_FILE)
    location_list = {item[-1] for item in training_data}
    perceptrons = [Perceptron(location) for location in location_list]

    for perceptron in perceptrons:
        a = random.sample(training_data, len(training_data))
        print("{}:".format(perceptron.location))
        perceptron.train_weights(a)
        print("weight_1 = {}, weight_2 = {}, weight_bias = {}".format(perceptron.weights[0],
            perceptron.weights[1], perceptron.weights[2]))


    for trained_perceptron in perceptrons:
        trained_perceptron.test(testing_data)
        trained_perceptron.printStats()


if __name__== "__main__":
    main()