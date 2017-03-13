import csv
import json
#list_i_want = ['id', 'handle', 'text', 'is_retweet', 'time']
#list_i_want = [0, 1, 2, 3, 5]

def askMala(message, candidate):
	print ""
	print "What do you think of this message by", candidate,  "(answer in percentage)"
	print message
	emotions = {}
	emotions["happiness"]   = raw_input("how happy is it?       ")
	emotions["excitement"]  = raw_input("how exciting is it?    ")
	emotions["hope"]        = raw_input("how hopeful is it?     ")
	emotions["love"]        = raw_input("how lovely is it?      ")
	emotions["sadness"]     = raw_input("how sad is it?         ")
	emotions["anger"]       = raw_input("how angry is it?       ")
	emotions["frustration"] = raw_input("how frustrating is it? ")
	emotions["disgust"]     = raw_input("how dsgusting is it?   ")
	return emotions

def extractTraining(f_reader):
	data = {}
	w = open('train_data.txt', 'w')
	for i in range(3):
		tweet = f_reader.next()
		while tweet[3] == True:
			tweet = f_reader.next()
		data[tweet[0]] = {}
		data[tweet[0]]['candidate'] = tweet[1]
		data[tweet[0]]['message'] = tweet[2]
		data[tweet[0]]['time'] = tweet[5]
		data[tweet[0]]['emotion'] = askMala(tweet[2], tweet[1])
	json.dump(data, w, indent=4)
	w.close()

def extractTest(f_reader):
	data = {}
	w = open('test_data.txt', 'w')
	for i in range(5):
		tweet = f_reader.next()
		while tweet[3] == True:
			tweet = f_reader.next()
		data[tweet[0]] = {}
		data[tweet[0]]['candidate'] = tweet[1]
		data[tweet[0]]['message'] = tweet[2]
		data[tweet[0]]['time'] = tweet[5]
		data[tweet[0]]['emotion'] = {}	
	json.dump(data, w, indent=4)
	w.close()

def interface():
	print "Hi Mala! There are 50 tweets to be analyzed. Let's Start!"
	f = open('tweets.csv', 'r')
	f_reader = csv.reader(f)
	f_reader.next()
	extractTraining(f_reader)
	extractTest(f_reader)
	f.close()

interface()