import sys
import itertools
import math
from collections import Counter

if len(sys.argv)>1:
	training_file=sys.argv[1]
	test_file=sys.argv[2]
else:
   	print 'Please provide both the training and test files as arguments to execute this program'
   
   
#Reading the contents of the training file   

with open(training_file, 'r') as inputFile:
	training_data = inputFile.readlines()


#################### TRAINING DATA PROCESSING #########################

unigrams_final_data=[]
bigrams=[]	   
   
'''Counting the number of hashes as the number of lines since we assume every sentence would start with a hash'''

count_hash=len(training_data)
#print 'Number of lines in the file is :', len(training_data)
	


################ CONSTRUCTION OF UNIGRAMS ###############################
'''Converting all data in the file to lower-case and splitting based on space to store the words Removing the '\n' from each line'''

for data in training_data:
	data1=data.lower();
	data2=data1.replace("\n","")
	data3=data2.split(" ")
	unigrams_final_data.append(data3)

#print 'Unigrams list is :', unigrams_final_data[:5]

#Unigrams is a list with all the words in the file split based on ""	

vocabulary_repeated=[]
unigrams_table={}

#Joining list of lists into a single list to get all words into a single list.Filtering out the '' because the file format was of the form a b c . \n

vocabulary_repeated=list(itertools.chain(*unigrams_final_data))
vocabulary_repeated = filter(lambda a: a != '', vocabulary_repeated)

#print 'After cleaning up:',vocabulary_repeated[:10]

#Creating dictionary of (word,count) key value pairs for the entire list or file of words

unigram_vocabulary=Counter(vocabulary_repeated)
unigrams_total_frequency=sum(unigram_vocabulary.values())

print 'Total unigram frequency:', unigrams_total_frequency

bigrams_vocabulary=Counter(vocabulary_repeated)

#Adding the (hash,count) value to the dictionary

bigrams_vocabulary['#']=count_hash
        
#print 'Vocabulary is :',bigrams_vocabulary   

print 'Number of times banjo occurs is :', unigram_vocabulary['banjo']     
        

################ UNIGRAM PROBABILITY FUNCTION ##########################

def unigrams_prob(sentence):

	prob_value=0
	data_array=sentence.split(" ")
	data_array = filter(lambda a: a != '', data_array)
	#print data_array
	for i in range(0, len(data_array)):
	
		#print 'word is:',data_array[i]
		#print 'Freq count of word:', unigram_vocabulary[data_array[i]]
		#print 'Total frequency count:',unigrams_total_frequency
		
		a=unigram_vocabulary[data_array[i]]
		b=unigrams_total_frequency
		
		if  a == 0:
			return 'undefined'
			break;
		else:
			prob_value += math.log(a/float(b),2)

	return prob_value



###################### TEST DATA PROCESSING ###############################

#Variable declarations

cleaned_data=[]


#Reading the contents of the test file   

with open(test_file, 'r') as inputFile2:
	test_data = inputFile2.readlines()


for data in test_data:
	data1=data.lower();
	data2=data1.replace("\n","")
	cleaned_data.append(data2)

for i in range(0, len(cleaned_data)):
  print 'S = ',cleaned_data[i]
  print 'Unigrams:logprob(S) = %.4f' %unigrams_prob(cleaned_data[i])
  '''print 'Bigrams:logprob(S) =', bigrams_prob(cleaned_data[i])
  print 'Smoothed Bigrams:logprob(S) =', smoothed_bigrams_prob(cleaned_data[i])'''	
	
	

