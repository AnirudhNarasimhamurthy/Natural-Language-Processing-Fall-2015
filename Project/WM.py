__author__ = 'Anirudh'

def wordMatch(question,sentence):
    question_words_set=set(question.split())
    sentence_words_set=set(sentence.split())

    [x.lower() for x in question_words_set]
    count=0
    for i in sentence_words_set:
        if i.lower() in [x.lower() for x in question_words_set]:
            count=count+1
    if count > 1:
        #print 'Question words set:',question_words_set
        #print 'Sentence words set:', sentence_words_set
        print 'No of words that appear in both question and sentence is',count
    return count