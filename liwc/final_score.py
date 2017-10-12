#Copyright 2017, Yuzhuang Chen
import json

# store the result from CNN
cnn_input_score = []

# store the user_liwc.json file
user_liwc = []
# has_user_liwc is to store the liwc score which is not zero from user_liwc 
has_user_liwc =[]

# store the get_score.json, the json data from get_score.py
get_score = []
# has_user_liwc is to store the get score which is not zero from user_liwc 
has_get_score = []

# This array is to store the top 3 best matched scores
best_matched = []

# Here is for getting the postive emotion and negative emotion
 	#pos_score.append(target_score['pos']['happiness'])
 	#pos_score.append(target_score['pos']['cheerful'])
 	#neg_score.append(target_score['neg']['depression'])
 	#neg_score.append(target_score['neg']['stressed'])

def get_total_weight(has_user_liwc):
	total_weight = 0
	number_indexs = 0
	for x in has_user_liwc:
		total_weight = total_weight + x[1]
		
	return total_weight	

#append a new data which is the weight of liwc score in the end of each has_user_liwc
def store_weight_ratio(has_user_liwc):
	total_weight = get_total_weight(has_user_liwc)
	for x in has_user_liwc:
		weight = (int(x[1])/float(total_weight))
		x.append(weight)
		#print(has_user_liwc)

#calculate_cnn_score(has_user_liwc, cnn_input_score)
def calculate_cnn_score(array1, array2):
	result = 0
	for x1 in array1:
		x2 = x1[0]
		for y1 in array2:
			if x2 == y1[0]:
				result = result + x1[2]*y1[1]
	return float(result)

#calculate_tweet_score(has_user_liwc, get_score)
def calculate_tweet_score(array1, array2):
	result = 0
	test = []
		
	for index in range(0, len(array2)):
		score = 0
		for arr1 in array1:
			key = arr1[0]
			
			for arr2 in range(0, len(array2[index])):
				if key == array2[index][arr2][0]:
					score = score + array2[index][arr2][1]*arr1[2]
				else:
					continue	
		array2[index].append(score)

		
			

# find_best_match(desired_score, get_score)
def find_best_match(score, array):
	matched_tweet = []
	for index in range(0, len(array)):
		matched_tweet.append([((array[index][-1] - score)*(array[index][-1] - score)),array[index][24][1]])
		
	matched_tweet.sort()
	print ('The best matched tweet is: {}, the score is: {}'.format(matched_tweet[0][1], matched_tweet[0][0])) 
	
	print ('The second best matched tweet is: {}, the score is: {}'.format(matched_tweet[1][1], matched_tweet[1][0])) 
	
	print ('The third best matched tweet is: {}, the score is: {}'.format(matched_tweet[2][1], matched_tweet[2][0])) 



if __name__ == '__main__':
	# read the cnn output json
	with open('cnn_test.json', 'r') as f:
		cnn_score = json.load(f)
		myitems = cnn_score.items()
		cnn_input_score = list(myitems)
		

	# read the user desired liwc score	
	with open('user_liwc.json', 'r') as f:
		target_score = json.load(f)
		myitems = target_score.items()
		user_liwc = list(myitems)
	
	for x in user_liwc:
		if x[1] != 0:
			has_user_liwc.append([x[0], x[1]])
		else:
			continue


	# read the tweet liwc score
	with open('get_score.json', 'r') as fp:
		
		tweet_score = json.load(fp)		
		for x in range(0, len(tweet_score)):
			myitems = tweet_score[x].items()
			get_score.append(myitems)
			
		
	store_weight_ratio(has_user_liwc)	

	desired_score = calculate_cnn_score(has_user_liwc, cnn_input_score)
	calculate_tweet_score(has_user_liwc, get_score)
	find_best_match(desired_score, get_score) 

	
	


	


