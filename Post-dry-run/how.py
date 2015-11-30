__author__ = 'Anirudh'

import WM
import NET
import nltk
nltk.data.path.append("/home/anirudhn/nltk_data")
import re
import POS_Tagging
from nltk.stem.wordnet import WordNetLemmatizer

# The selection of answer is based on the sentence which gets the maximum total score across the four conditions ##

# But generally answers to "when" questions almost always involves a time expression, so sentences that do not contain a time
# expression are only considered in special cases

def answering_how(cleansedQuestion,stop_words_free_question,complete_sentence_list,sentence_list,sent_time_list,sent_percent_list):

    # Declaring globals to be used in this function

    candidate_sent_list=[]
    sent_score_list=[]
    final_sent_list=[]
    q_verblist=[]
    best=[] # List of the best scoring sentences based on word match with the question


    much_list=['thousand','hundred','dollars','cents','million','billion','trillion','none','nothing','everything','few','something',
               'cent','percent','salary','pay','income','loss','profit','one','two','three','four','five','six','seven','eight','nine','ten',
               'twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']

    many_list=['one','two','three','four','five','six','seven','eight','nine','ten',
               'twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety','hundred',
               'thousand','million','billion','trillion']

    how_often=['daily','weekly','bi-weekly','fortnightly','monthly','bi-monthly','quarterly','half-yearly','yearly','decade','millennium'
               'day','everyday','night','afternoon','noon']
    nums = re.compile(r"[+-]?\d+(?:\.\d+)?")

    measurement_verbs=[]

    stanford_stop_words_list=['a','an','and','are','as','at','be','buy','do','for','from',
                          'has','have','he','in','is','it','its','of','on','that','the',
                          'to','was','were','will','with']

    abbreviation_list=[('Mt.','Mount')]


    ########################### QUESTION PROCESSING ##################

    temp_q=cleansedQuestion
    #temp_q=temp_q.replace('"','')
    #temp_q=temp_q.replace("'",'"')
    temp_q=temp_q.replace('?','')

    for k in temp_q.split():
        if k in abbreviation_list[0][0]:
            temp_q=temp_q.replace(k,abbreviation_list[0][1])

    #print 'Question is :',temp_q


    lmtzr=WordNetLemmatizer()
    pos_list= POS_Tagging.pos_tagging(temp_q)

    for i in range(0, len(pos_list)):
        if pos_list[i][1] in ['VB','VBD','VBZ','VBN'] and lmtzr.lemmatize(pos_list[i][0],'v') not in stanford_stop_words_list:
            q_verblist.append(lmtzr.lemmatize(pos_list[i][0],'v'))

    #print 'Question verb list is :',q_verblist

    #print 'Time list is:',sent_time_list

    ################## SENTENCE PROCESSING AND SCORING ###################

    for i in range(0,len(complete_sentence_list)):
        score=0

        # 1. Find score for each sentence using word march score first

        #print 'The sentence is :',complete_sentence_list[i]
        #score = score + WM.stemWordMatch(cleansedQuestion,sentence_list[i])
        score = score + WM.stemWordMatch(stop_words_free_question,sentence_list[i])



        #2. If the question contains "many" and sentence contains an expression of number, then it is confident score

        for k in temp_q.split():
            if k.lower()=="many":
                for m in complete_sentence_list[i].split():
                    if nums.match(m) or m in many_list:
                        score=score + 6

            #3. If the question contains "much" and sentence contains an expression for distance or for money, then it is a confident score
            elif k.lower()=="much":
                for m in complete_sentence_list[i].split():
                    if m.lower()  in ['money','earn','salary','profit','loss'] or m in much_list:
                        score=score+6

            #4. If the question contains "often" and sentence contains an expression of time, then it is more than confident score
            elif k.lower()=="often":
                for m in complete_sentence_list[i].split():
                    if m.lower()  in sent_time_list or m.lower() in how_often:
                        score=score+10

        '''if much_flag==1 and money_flag==1:
            temp2=complete_sentence_list[i].split()
            #print temp2
            for k in range(0, len(temp2)):
                if temp2[k] in much_list:
                    score=score +20 #slam-dunk

        elif much_flag==1:

            temp2=complete_sentence_list[i].split()
            #print temp2
            for k in range(0, len(temp2)):
                if nums.match(temp2[k]) or temp2[k] in much_list:   # Implies answer contains a number
                    #print 'much Q - number or list sentence'
                    score=score+6'''

        sent_score_list.append(score)

    #print 'Score list is:',sent_score_list
    max_score_value=max(sent_score_list)

    # Finding the sentences which has the highest score and adding them to the best list

    for i in range(0,len(sentence_list)):
        if sent_score_list[i]==max_score_value:
            final_sent_list.append(complete_sentence_list[i])

    #print 'Final sent list is:',final_sent_list

    temp_result=[]
    temp_solution=[]
    if len(final_sent_list) == 1:

        #If the question contains often, the sentence will usually contain a time expression.If so pick
        #that expression as the solution

        '''temp=cleansedQuestion.split()
        if 'often' in temp:
            #print 'often'
            temp2=final_sent_list[0].split()
            for m in range(0,len(temp2)):
                if temp2[m] in how_often:
                    temp_solution.append(temp2[m])
            #print 'Answer: ',' '.join(temp_solution)+'\n'
            #print '\n'
            return ' '.join(temp_solution)'''

        if 'many' in temp_q.split():
            #print 'many'
            temp2=final_sent_list[0].split()
            for m in range(0,len(temp2)):
                if nums.match(temp2[m]) or temp2[m] in many_list:
                    temp_solution.append(temp2[m])

            return ' '.join(temp_solution)

        return final_sent_list[0]


        '''for k in final_sent_list[0].split():
            if k not in cleansedQuestion.split():
                temp_result.append(k)

        return ' '.join(temp_result)'''


    else:
        # Choose the sentence that comes at the last, in case of a tie
        for k in range(0,len(final_sent_list)):
            result=final_sent_list[k]
            break

        for k in result.split():
            if k not in cleansedQuestion.split():
                temp_result.append(k)

        return ' '.join(temp_result)


