# Tweet-Tone

1. Run tweet-tone-analyser.py with the tweets.csv. 
2. tweets.csv is the csv file that contains a good sample of 1000 tweets across the 2 candidates and over the time period. 
3. With this script, you would be able to train vast amounts of data manually, ensuring a very strong baseline for which the predictor to base upon. 
4. Run tone_learner.py. This takes in the train_data.txt outputted by the previous step and learn all the weights based on the trained data. Then it outputs unigram_weights and bigram_weights. 
5. Run tone_predictor.py which takes in the test_data.txt and prints out the predictions of the sentiment analysis to your console. 
