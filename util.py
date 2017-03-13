import random
import collections
import math
import sys
import itertools
from collections import Counter
from util import *

def extractWordFeatures(x):
    dictionary = collections.defaultdict(int)
    for word in x.split(): dictionary[word] += 1
    return dict(dictionary)

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    weights = {}  # feature => weight
    for iteration in range(numIters):
        for train_example in trainExamples:
            feature_vector = featureExtractor(train_example[0])
            weights.update({word:0 for word in train_example[0].split() if word not in weights})
            margin = dotProduct(weights, feature_vector) * train_example[1]
            eta_y = eta * train_example[1] if margin < 1 else 0
            increment(weights, eta_y, feature_vector)
        trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        devError = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        print "iteration %s: train error = %s, dev error = %s" % (iteration+1, trainError, devError)
    return weights

def generateDataset(numExamples, weights):
    random.seed(42)
    def generateExample():
        phi = {key: (random.uniform(-0.5,0.5)) for key in weights if random.random() > 0.1}
        y = 1 if dotProduct(weights, phi) > 0 else -1
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

def extractCharacterFeatures(n):
    def extract(x):
        x = x.replace(' ', '')
        feature_vector = collections.defaultdict(int)
        while len(x) > n:
            feature_vector[x[0:n]] += 1
            x = x[1:]
        if len(x) <=n:
            feature_vector[x] += 1
        return dict(feature_vector)
    return extract

import datetime

def kmeans(examples, K, maxIters):
    # BEGIN_YOUR_CODE (our solution is 32 lines of code, but don't worry if you deviate from this)
    # assignments = [None]*len(examples)
    #Step 0: Initialize random centroids using partial K++ (use training points)
    #Stragely, examples will update together with centroids, returning dense vectors
    # centroids = random.sample(list(examples), K)
    # prev_assignments, prev_centroids = list(assignments), list(centroids)
    # #Iteration
    # for iters in range(maxIters):
    #     # Step 1: Find assignments
    #     d1=datetime.datetime.now()
    #     evaluate = [0]*K
    #     for example_iter in range(len(examples)):
    #         examples_i = {k:v for k,v in examples[example_iter].iteritems() if v!=0}
    #         for centroid_iter in range(len(centroids)):
    #             centroid_focus = dict(centroids[centroid_iter])
    #             increment(centroid_focus, -1, examples_i)
    #             evaluate[centroid_iter] = dotProduct(centroid_focus, centroid_focus)
    #         assignments[example_iter] = evaluate.index(min(evaluate))
    #     d2=datetime.datetime.now()
    #     print 'step1', d2-d1
    #     # Step 2: Find centroids (optimization)
    #     d1=datetime.datetime.now()
    #     for centroid_iter in range(len(centroids)):
    #         if centroid_iter not in assignments: continue
    #         counter, new_centroid = 0, {}
    #         for example_iter in range(len(examples)):
    #             if assignments[example_iter]==centroid_iter:
    #                 counter += 1
    #                 increment(new_centroid, 1, examples[example_iter])
    #         factorized_centroid = {}
    #         increment(factorized_centroid, 1.0/counter, new_centroid)
    #         centroids[centroid_iter] = factorized_centroid
    #     d2=datetime.datetime.now()
    #     print 'step2', d2-d1
    #
    #     if sorted(prev_centroids) == sorted(centroids) and sorted(prev_assignments) == sorted(assignments): break
    #     else: prev_centroids, prev_assignments = list(centroids), list(assignments)
    # # Step 3: Calculate loss
    # loss = 0
    # for example_iter in range(len(examples)):
    #     focus = dict(examples[example_iter])
    #     increment(focus, -1, centroids[assignments[example_iter]])
    #     loss += dotProduct(focus, focus)
    # return centroids, assignments , loss
    # raise Exception("Not implemented yet")
    #distance is just total of squared distance
    def distance(x1, x2):
        result = 0
        for f, v in x2.items():
            result += (x1.get(f, 0) - v) ** 2
        return result
    #average 
    def average(points):
        n = float(len(points))
        result = {}
        for p in points:
            increment(result, 1 / n, p)
        return result

    centroids = random.sample(examples, K)
    old_assignments = []
    for _ in range(maxIters):
        center_points_pair = []
        assignments = []
        totalCost = 0
# ## map phase:
        for p in examples:
            dis = [distance(c, p) for c in centroids]
            newCenter = dis.index(min(dis))
            assignments.append(newCenter)
            totalCost += min(dis)
#           print dis, newCenter
            center_points_pair.append((newCenter, p))
        if assignments == old_assignments:
            break
        else:
            old_assignments = list(assignments)
        center_points_pair = sorted(center_points_pair, key=lambda item: item[0])
# ## reduce phase with groupby() and average():
        new_centroids = []
        for key, kpList in itertools.groupby(center_points_pair, key=lambda item:item[0]):
            pList = [ kp[1] for kp in kpList]
            new_centroids.append(average(pList))

#       print 'new centroids are', new_centroids
        centroids = new_centroids
#   print centroids, assignments, totalCost
    return centroids, assignments, totalCost
    # END_YOUR_CODE
