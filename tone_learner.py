import json
import re
import collections

def learning(file_name):
	with open(file_name) as json_file:
		focus = json.load(json_file)
		# print (focus)

	weight_unary = {}
	weights = {}
	for key_id in focus:
		text_to_learn = focus[key_id]["message"]
		text_list = re.split('[ ,.:!]', text_to_learn)
		text_again = []
		for text in text_list:
			if text.startswith('http'): continue
			if re.search('[a-zA-Z]', text) == None: continue
			if '/' in text: continue
			text_again.append(text.encode('utf-8').lower())
		# print text_again

		if text_again[0] not in weight_unary:
			weight_unary[text_again[0]] = collections.defaultdict(int)
		weight_unary[text_again[0]]['freqeuncy'] += 1
		for emotion in focus[key_id]['emotion']:
			weight_unary[text_again[0]][str(emotion)] += int(focus[key_id]['emotion'][emotion])
		for index in range(len(text_again) - 1):
			word_pair = (text_again[index], text_again[index+1])
			if text_again[index+1] not in weights:
				weight_unary[text_again[index+1]] = collections.defaultdict(int)
			weight_unary[text_again[index+1]]['freqeuncy'] += 1
			if word_pair not in weights:
				weights[word_pair] = collections.defaultdict(int)
			weights[word_pair]['freqeuncy'] += 1
			for emotion in focus[key_id]['emotion']:
				weight_unary[text_again[index+1]][str(emotion)] += int(focus[key_id]['emotion'][emotion])
				weights[word_pair][str(emotion)] += int(focus[key_id]['emotion'][emotion])
	
	# print weight_unary
	w = open('unary-weight.txt', 'w')
	for word in weight_unary:
		freqeuncy = weight_unary[word]['freqeuncy']
		for emotion in weight_unary[word]:
			if emotion == 'freqeuncy': continue
			weight_unary[word][emotion] /= float(freqeuncy)
		w.write(word + "   " + str(dict(weight_unary[word])) + '\n')
	w.close()
	
	w2 = open('binary-weight.txt', 'w')
	for word_pair in weights:
		freqeuncy = weights[word_pair]['freqeuncy']
		for emotion in weights[word_pair]:
			if emotion == 'freqeuncy': continue
			weights[word_pair][emotion] /= float(freqeuncy)
		w2.write(str(word_pair) + "   " + str(dict(weights[word_pair])) + '\n')
	w2.close() 

learning('train_data.txt')
