__author__ = 'Anirudh'

import WM
import NET
import nltk
nltk.data.path.append("/home/anirudhn/nltk_data")
from nltk.stem.wordnet import WordNetLemmatizer
import POS_Tagging

# The selection of answer is based on the sentence which gets the maximum total score across the four conditions ##

# But generally answers to "when" questions almost always involves a time expression, so sentences that do not contain a time
# expression are only considered in special cases

def answering_why(cleansedQuestion,stop_words_free_question,complete_sentence_list,sentence_list):

    # Declaring globals to be used in this function

    sent_score_list=[]
    final_sent_list=[]
    best_sent_index=[]
    best=[] # List of the best scoring sentences based on word match with the question
    q_verblist=[]


    stanford_stop_words_list=['a','an','and','are','as','at','be','buy','do','for','from',
                          'has','have','he','in','is','it','its','of','on','that','the',
                          'to','was','were','will','with']

    temp_q=cleansedQuestion
    temp_q=temp_q.replace('"','')
    temp_q=temp_q.replace("'",'"')
    temp_q=temp_q.replace('?','')

    #print 'Question is :',temp_q


    lmtzr=WordNetLemmatizer()
    pos_list= POS_Tagging.pos_tagging(temp_q)

    for i in range(0, len(pos_list)):
        if pos_list[i][1] in ['VB','VBD','VBZ','VBN','VBP'] and lmtzr.lemmatize(pos_list[i][0],'v') not in stanford_stop_words_list:
            q_verblist.append(lmtzr.lemmatize(pos_list[i][0],'v'))

    #print 'Question verb list is :',q_verblist


    # Find score for each sentence using word march score first

    for i in range(0,len(complete_sentence_list)):
        wm_score=0
        #complete_sentence_list[i]=complete_sentence_list[i].replace('.','').replace(',','').replace('!','')

        wm_score = wm_score + WM.stemWordMatch(cleansedQuestion,sentence_list[i])
        sent_score_list.append(wm_score)


    max_score_value=max(sent_score_list)
    #print 'Max score is :',max_score_value

    # Finding the sentences which has the highest score and adding them to the best list

    for i in range(0,len(sentence_list)):
        if sent_score_list[i]==max_score_value:
            best.append((complete_sentence_list[i],i))
            best_sent_index.append(i)

    #print 'Best list is:',best


    # Finding indices of the best sentences

    # Re-setting the scores of all sentences to zero
    for i in range(0, len(sent_score_list)):
        sent_score_list[i]=0


    for i in range(0, len(complete_sentence_list)):
        score=0
        # 1. If the given sentence is in the best list, then reward them. It is a clue
        if i in best_sent_index:
            score=score + 3

        #2. If the sentence immediately precedes member of best, then it is a clue

        for k in best_sent_index:
            #print k
            if i==k-1:
                score=score + 3
            #3. If the sentence immediately follows member of best, then it is a good clue
            elif i==k+1:
                score=score + 4

        #4. If the sentence contains word "want", then it is a good clue
        temp=complete_sentence_list[i].split()
        for word in temp:
            if word.lower()=='want':
                score=score+4
            #5. If the sentence contains word "so" or "because"  then it is a good clue
            elif word.lower() in ['so','because']:
                score=score+4

        #5. Matching the main verb in question and sentence. If so it is a confident clue

        sent_pos_list=POS_Tagging.pos_tagging(complete_sentence_list[i])
        lmtzr=WordNetLemmatizer()
        for k in range(0, len(sent_pos_list)):
            if sent_pos_list[k][1] in ['VB','VBD','VBZ','VBN'] and lmtzr.lemmatize(sent_pos_list[k][0],'v') in q_verblist:
                #print 'Verb in question and sentence matches'
                score=score + 6


        sent_score_list[i]=score

    #print 'Sent score list values are:',sent_score_list


    # Selecting the sentence that has the maximum score.

    max_score_value =max(sent_score_list)
    #print 'Max value is :', max_score_value


    # Now we have to choose the best sentence among the sentences in candidate list. Choosing sentences
    # which have both maximum value and present in candidate list. For why questions we don't do more filtering
    # since most of the answers span the entire sentence

    for i in range(0, len(sent_score_list)):
         if sent_score_list[i]==max_score_value:
                final_sent_list.append(complete_sentence_list[i])

    #print 'Final list is:', final_sent_list

    if len(final_sent_list) == 1:
        temp=final_sent_list[0].split()
        for k in range(0, len(temp)):
            if temp[k].lower() =='so':                         #If sentence contains "so", the answer is generally the words that come after so
                return ' '.join(temp[k:])
            if temp[k].lower() =='because':                         #If sentence contains "because", the answer is generally the words that come after because
                return ' '.join(temp[k:])
            if temp[k].lower() =='to':                         #If sentence contains "to", the answer is generally the words that come after so
                return ' '.join(temp[k:])

        return final_sent_list[0]

    else:
        # Choose the sentence that comes at the last, in case of a tie
        for k in range(0,len(final_sent_list)):
            result=final_sent_list[k]

        return result





