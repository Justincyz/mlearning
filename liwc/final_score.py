#Copyright 2017, Yuzhuang Chen
import json
import math
#The tweet score which closest to target score is: 0.0882355861847 Justin know relaxing Kauai at Martin Luther King, Jr. Da. Moreover, Justin hear dirge is talking about exciting Utopia at Martin Luther King, Jr. Day
# store the result from CNN

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
def target_error(score, array):
	matched_tweet = []
	for index in range(0, len(array)):
		matched_tweet.append([(array[index][-1] - score),array[index][24][1]])
		
# matched_tweet[0] is the best matched tweet	
	matched_tweet.sort()
	return matched_tweet


def find_best_pair(library1, library2):
	negative_library1 = []
	positive_library1 = []
	negative_library2 = []
	positive_library2 = []
	shortest_library = []
	combined_library = []

	for index in range(0, len(library1)):
		if(library1[index][0] < 0):
			negative_library1.append([library1[index][0], library1[index][1]])
		else:	
			positive_library1.append([library1[index][0], library1[index][1]])

	for index in range(0, len(library2)):
		if(library2[index][0] < 0):
			negative_library2.append([library2[index][0], library2[index][1]])
		else:	
			positive_library2.append([library2[index][0], library2[index][1]])		

	shortest_library.append(len(negative_library1))
	shortest_library.append(len(positive_library1))
	shortest_library.append(len(negative_library2))
	shortest_library.append(len(positive_library2))
	shortest_library.sort()

	negative_library1.sort()
	positive_library1.sort()
	negative_library2.sort()
	positive_library2.sort()
	

	for index in range (0, shortest_library[0]):
		score = negative_library1[len(negative_library1) - 1- index][0]
		for index1 in range(0, shortest_library[0]):
			score1 = (score + positive_library2[index1][0])/2
			combined_library.append([score1, negative_library1[len(negative_library1) - 1- index][1], positive_library2[index1][1]])

	for index in range (0, shortest_library[0]):
		score = negative_library2[len(negative_library2) - 1 -index][0]
		for index1 in range(0, shortest_library[0]):
			score1 = (score + positive_library1[index1][0])/2
			combined_library.append([score1, negative_library2[len(negative_library2) - 1 -index][1], positive_library1[index1][1]])		

	combined_library.sort()
	#print combined_library
	find_best_pair_helper(combined_library)		

		
def find_best_pair_helper(matched_tweet):
	best_matched = matched_tweet[0][0]
	best_matched1 = None
	tweet1 = ''
	tweet2 = ''

	for index in range (0,len(matched_tweet)):
		if abs(matched_tweet[index][0]) < abs(best_matched):
			best_matched = abs(matched_tweet[index][0])
			best_matched1 = matched_tweet[index][0]
			tweet1 = matched_tweet[index][1]
			tweet2 = matched_tweet[index][2]
			
		else:
			continue			


	print best_matched
	print tweet1
	print tweet2



if __name__ == '__main__':
	cnn_input_score = []

# store the user_liwc.json file
	user_liwc = []
# has_user_liwc is to store the liwc score which is not zero from user_liwc 
	has_user_liwc = []

# store the get_score.json, the json data from get_score.py
	get_score = []
	get_score1 = []

# Two libraries after we associate a distance score for each tweet 
	library1 = []
	library2 = [] 

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
	with open('library1.json', 'r') as fp:
		tweet_score = json.load(fp)		
		for x in range(0, len(tweet_score)):
			myitems = tweet_score[x].items()
			get_score.append(myitems)
	
	with open('library2.json', 'r') as fp:
		tweet_score = json.load(fp)		
		for x in range(0, len(tweet_score)):
			myitems = tweet_score[x].items()
			get_score1.append(myitems)


		
	store_weight_ratio(has_user_liwc)	

	desired_score = calculate_cnn_score(has_user_liwc, cnn_input_score)
	calculate_tweet_score(has_user_liwc, get_score)
	library1 = target_error(desired_score, get_score) 

	calculate_tweet_score(has_user_liwc, get_score1)
	library2 = target_error(desired_score, get_score1)

	find_best_pair(library1, library2)



	
	


	


