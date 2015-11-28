__author__ = 'Anirudh'

import nltk
nltk.data.path.append("/home/anirudhn/nltk_data")
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer




def stemWordMatch2(question,sentence):


    question_tokens = set(nltk.word_tokenize(question))
    sentence_tokens=set(nltk.word_tokenize(sentence))

    #  Finding the match between two words from the same root  using Lancaster Stemmizer

    '''stemmer=LancasterStemmer()

    for i in sentence_tokens:
        stem_words_list.append(stemmer.stem(i))

    for i in question_tokens:
        question_words_list.append(stemmer.stem(i))

    #print 'Stem word list',stem_words_list
    #print 'Question word list', question_words_list

    stem_count=0
    for i in stem_words_list:
        #Finding the exact word match
        if i.lower() in [x.lower() for x in question_words_list]:
            #print 'Question word is',x
            #print 'Sentence word stem is :',i
            #print 'Match'
            stem_count=stem_count+6
    stem_word_match_counter.append(count)'''

    stem_word_match_counter=[]
    stem_words_list=[]
    question_words_list=[]

    #  Finding the match between two words from the same root  using Snowball Stemmizer

    snowball_stemmer = SnowballStemmer('english')

    for i in sentence_tokens:
        stem_words_list.append(snowball_stemmer.stem(i))

    for i in question_tokens:
        question_words_list.append(snowball_stemmer.stem(i))

    #print 'Stem word list',stem_words_list
    #print 'Question word list', question_words_list

    stem_count=0
    for i in stem_words_list:
        #Finding the exact word match
        if i.lower() in [x.lower() for x in question_words_list]:
            #print 'Question word is',x
            #print 'Sentence word stem is :',i
            #print 'Match'
            stem_count=stem_count+6
    #print 'Stem word count match score is :', stem_count

    return stem_count



def stemWordMatch(question,sentence):

    #snowball_stemmer = SnowballStemmer('english')

    #print 'Inside stemWordMatch'

    lmtzr = WordNetLemmatizer()

    question_tokens = set(nltk.word_tokenize(question))
    sentence_tokens=set(nltk.word_tokenize(sentence))

    #print 'Question is :',question_tokens
    #print 'Sentence is :',sentence_tokens
    count=0
    for i in sentence_tokens:
        #Finding the exact word match
        if lmtzr.lemmatize(i, 'v').lower() in  [lmtzr.lemmatize(x, 'v').lower() for x in question_tokens]:
            count=count+6
        elif i.lower() in [x.lower() for x in question_tokens]:
            count=count+3
    #print 'Exact word match count is :',count
    return count


