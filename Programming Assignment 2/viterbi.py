import sys
import itertools
import math
import random
import operator
from collections import Counter

#Basic command line arguments error checking and storing input data

if len(sys.argv)>1:
	probabilities_file=sys.argv[1]
	sentences_file=sys.argv[2]
else:
   	print 'Please provide the probabilities file and sentences file as inputs to the program in the specified order <probabilities_file>, <sentences_file>'
     

########## Variables declaration   #################

words_sent=[] #List of lists to store each sentence's words
W=0  #Number of words in the sentence
pos_tags=['noun','verb','inf','prep']
T=len(pos_tags) # In this case we have only four POS tags + phi symbol
prob_data_list=[]
prob_dict={}


   
#Reading the contents of the probabilities file   

with open(probabilities_file, 'r') as inputFile:
	prob_data = inputFile.readlines()

for i in range(0, len(prob_data)):
	prob_data_list.append(prob_data[i].replace('\n','').split(" "))
	
#print 'Probabilities values are :', prob_data_list


# Storing the values from the probabilities file as a dictionary of key,value pairs where key is POS bigram /lexical generation pairs

for i in range(0, len(prob_data_list)):
	key=(prob_data_list[i][0],prob_data_list[i][1])
	value=float(prob_data_list[i][2])
	prob_dict[key]=value

#print 'The prob dict values are :', prob_dict	
	


############################ VITERBI ALGORITHM ################################


def viterbi(sent, W, T):

	score=[[0 for x in range(W)]  for i in range(T)]
	backptr=[[0 for x in range(W)]  for i in range(T)]
	#print 'Score is :', score
	#print 'No of tags is :', T
	
	print '\nFINAL VITERBI NETWORK'
	###############   Initialization step   ###################
	for t in range(0, T):
		word1_tagt=(sent[0],pos_tags[t])
		#print 'Word1 | tag_t is :', word1_tagt
		tagt_phi=(pos_tags[t],'phi')
		#print 'Tag_t | phi is :', tagt_phi
		
		# Four possible cases handled below
		
		if word1_tagt in prob_dict:
			if tagt_phi in prob_dict:
				score[t][0]=prob_dict[word1_tagt] * prob_dict[tagt_phi] #Both are in dict
			else:
				score[t][0]=prob_dict[word1_tagt] * 0.001   #tagt_phi is not in dict
		else:
			if tagt_phi in prob_dict:
				score[t][0]= 0.0001 * prob_dict[tagt_phi]	#word1_tagt is not in dict
			else:
				score[t][0]= 0.0001 * 0.0001	            # both are not in dict
				
		# Updating the backptr network
		
		backptr[t][0]=0		

		print 'P(' + sent[0] + '=' + pos_tags[t] +') = %.10f' %score[t][0]


	##################### Iteration step #####################

	max_value_candidates=[]
	pos=0
	for w in range(1, len(sent)):
		for t in range(0, T):
			wordw_tagt=(sent[w],pos_tags[t])   #wordw | tagt
			
			# Implementing MAXj=1,T (Score(j, w-1) * Pr(Tagt | Tagj)) #
			for j in range(0,T):
				
				tagt_tagj=(pos_tags[t],pos_tags[j])
				if tagt_tagj in prob_dict:
		
					value= score[j][w-1] * prob_dict[tagt_tagj]
				else:
					value=	score[j][w-1] * 0.0001    #If the bigram is not there, use the default value
			
				max_value_candidates.append(value)	
			
			#Finding the max value from the list
			max_value=0;
		
			for i in range(0, len(max_value_candidates)):
				if(max_value_candidates[i] > max_value):
					max_value=max_value_candidates[i]
					pos=i
					
			#print 'Postion is :', pos
			
			#max_value=max(max_value_candidates)  
			
			
			max_value_candidates=[]   
			
			if wordw_tagt in prob_dict:
				
				score[t][w]=prob_dict[wordw_tagt] * max_value
			else:
				
				score[t][w]=0.0001 * max_value
				
			backptr[t][w]=pos	
		
			print 'P(' + sent[w] + '=' + pos_tags[t] +') = %.10f' %score[t][w]	
	
	print '\nFINAL BACKPTR NETWORK'
	for w in range(1, len(sent)):
		for t in range(0, T):		
			print 'Backptr(' + sent[w] +'=' +pos_tags[t] +')=', pos_tags[backptr[t][w]]	
			
			
######################## SEQUENCE IDENTIFICATION #####################################

			
				
############################# SENTENCE FILE PROCESSING #################################

# Reading the contents of the sentences file

with open(sentences_file, 'r') as inputFile:
	sent_data = inputFile.readlines()

for i in range(0, len(sent_data)):
	sent_data[i]=sent_data[i].replace('\n', '').lower()
	
print 'Sentences values are :', sent_data


# Storing the words in each sentence in a list of lists

for i in range(0, len(sent_data)):
	words_sent.append(sent_data[i].split(" "))
	
#print 'Words sent is:', words_sent	

for i in range(0, len(words_sent)):
	print 'PROCESSING SENTENCE:', ' '.join(words_sent[i])
	W=len(words_sent[i])
	#print 'No of words in the sentence is :', W
	viterbi(words_sent[i],W,T)