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
     

# Variables declaration   

words_sent=[] #List of lists to store each sentence's words
W=0  #Number of words in the sentence
T=5 # In this case we have only four POS tags + phi symbol
prob_data_list=[]
prob_dict={}
   
#Reading the contents of the probabilities file   

with open(probabilities_file, 'r') as inputFile:
	prob_data = inputFile.readlines()

for i in range(0, len(prob_data)):
	prob_data_list.append(prob_data[i].replace('\n','').split(" "))
	
print 'Probabilities values are :', prob_data_list


# Storing the values from the probabilities file as a dictionary of key,value pairs where key is POS bigram /lexical generation pairs

#Creating a list of lists first

'''for i in range(0, len(prob_data)):
	prob_data_list.append(prob_data[i].split(" "))'''

#Creating the dictionary of key,value pairs here
for i in range(0, len(prob_data_list)):
	key=(prob_data_list[i][0],prob_data_list[i][1])
	value=float(prob_data_list[i][2])
	prob_dict[key]=value

print 'The prob dict values are :', prob_dict	
	

# Reading the contents of the sentences file

with open(sentences_file, 'r') as inputFile:
	sent_data = inputFile.readlines()

for i in range(0, len(sent_data)):
	sent_data[i]=sent_data[i].replace('\n', '')
	
#print 'Sentences values are :', sent_data


# Storing the words in each sentence in a list of lists

for i in range(0, len(sent_data)):
	words_sent.append(sent_data[i].split(" "))
	
#print 'Words sent is:', words_sent	

for i in range(0, len(words_sent)):
	print 'PROCESSING SENTENCE:', ' '.join(words_sent[i])
	W=len(words_sent[i])
	print 'No of words in the sentence is :', W