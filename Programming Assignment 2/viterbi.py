import sys
import itertools
import math
import random
import operator
from collections import Counter

if len(sys.argv)>1:
	probabilities_file=sys.argv[1]
	sentences_file=sys.argv[2]
else:
   	print 'Please provide the probabilities file and sentences file as inputs to the program in the specified order <probabilities_file>, <sentences_file>'
   
   
#Reading the contents of the training file   

with open(probabilities_file, 'r') as inputFile:
	prob_data = inputFile.readlines()
