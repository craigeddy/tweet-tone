import json
import collections
import re
import ast

def getUnaryWeights():
	unary_weight = {}
	f = open('unary-weight.txt', 'r')
	for line in f:
		params = line.split('   ')
		unary_weight[params[0]] = ast.literal_eval(params[1])

	f.close()
	return unary_weight

def getBinaryWeights():
	binary_weight = {}
	f = open('binary-weight.txt', 'r')
	for line in f:
		params = line.split('   ')
		binary_weight[params[0]] = params[1]
	f.close()
	return binary_weight

def predicting(file_name):
	unary_weights = getUnaryWeights()
	binary_weights = getBinaryWeights()
	with open(file_name) as json_file:
		focus = json.load(json_file)

	for key_id in focus:
		message = focus[key_id]["message"].encode('utf-8')
		emotions = {'sadness': 0.0, 'disgust': 0.0, 'anger': 0.0, 'joy': 0.0, 'fear': 0.0}
		text_list = re.split('[ ,.:!]', message)
		text_again = []

		for text in text_list:
			if text.startswith('http'): continue
			if re.search('[a-zA-Z]', text) == None: continue
			if '/' in text: continue
			text_again.append(text.encode('utf-8').lower())

		compare_times = 0
		if text_again[0] in unary_weights:
			compare_times += 1
			for emotion in emotions:
				emotions[emotion] += unary_weights[text_again[0]][emotion]
		for index in range(len(text_again)-1):
			if text_again[index+1] in unary_weights:
				compare_times +=1
				for emotion in emotions:
					emotions[emotion] += unary_weights[text_again[index+1]][emotion]
			w_pair = (text_again[index], text_again[index+1])
			if w_pair in binary_weights:
				compare_times +=1
				for emotion in emotions:
					emotions[emotion] += binary_weights[w_pair][emotion]

		if compare_times > 0:
			for emotion in emotions:
				emotions[emotion] /= compare_times

		print message
		print emotions
		print


predicting('test_data.txt')