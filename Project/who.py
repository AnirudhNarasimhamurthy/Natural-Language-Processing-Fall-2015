__author__ = 'Anirudh'

import WM
import NET
import nltk
#nltk.data.path.append("/home/alangar/nltk_data")
from nltk.stem import SnowballStemmer

# The selection of answer is based on the sentence which gets the maximum total score across the four conditions ##

# But generally answers to "who" questions involve a person and so the maximum priority is given to them than other sentences


def answering_who(cleansedQuestion,stop_words_free_question,sentence_list):

    # Declaring globals to be used in this function

    wordmatch_score_list=[]
    sent_containing_person_score_list=[]
    sent_containing_name_score_list=[]
    sent_containing_person_and_name_score_list=[]
    sent_containing_person_or_name_score_list=[]
    master_person_list=[]
    sent_score_list=[]

    #print 'Question is :',cleansedQuestion

    snowball_stemmer = SnowballStemmer('english')

    for i in range(0, len(sentence_list)):
        #print 'Sentence is :', sentence_list[i]
        score=0
        # 1. Score using word match rule
        wordmatch_score_list.append(WM.stemWordMatch(cleansedQuestion,sentence_list[i]))
        score=score + WM.stemWordMatch(cleansedQuestion,sentence_list[i])

        # 2. If question does not contain name but the answer contains NAME then you are confident(+6)
        q_person_list,org_list,loc_list,time_list,prof_list = NET.named_entity_tagging(cleansedQuestion)
        if q_person_list==[]:
            sent_plist,sent_olist,sent_llist,sent_tlist,sent_proflist=NET.named_entity_tagging(sentence_list[i])
            master_person_list.append((sent_plist,i))
            if sent_plist !=[]:
                score=score + 6*len(sent_plist)

            # 3. If question does not contain a name and answer contains the word "name" then good_clue (+4)
            temp= sentence_list[i].split()
            for k in range(0,len(temp)):
                if snowball_stemmer.stem(temp[k].lower())=='name':
                    score=score +4

        else:
            #Question has a name, and if the sentence contains the same name, then it is a good clue.

            #  4. Awards points to all sentences  that contain a name or reference to a human
            sent_plist,sent_olist,sent_llist,sent_tlist,sent_proflist=NET.named_entity_tagging(sentence_list[i])
            master_person_list.append(sent_plist)
            if sent_plist==q_person_list:
                score=score+4*len(sent_plist)

            elif sent_plist != [] or "name" in sentence_list[i]:
                score=score+4

            '''if sent_plist==[] and "name" in sentence_list[i]:
                sent_containing_name_score_list.append(4)
            else:
                sent_containing_name_score_list.append(0)'''
        sent_score_list.append(score)

    #print 'Sent score list is :',sent_score_list
    #print 'Master person list is:',master_person_list

    # Selecting the sentence that has the maximum score. If it is a tie, we choose the sentence that appears first
    # Preference is given to sentences which have a person name in them. If there is only one such sentence that is the answer


    candidate_list=[]
    final_result_set=[]
    temp_list=[]

    max_score_value=max(sent_score_list)

    #print 'Max score is :',max_score_value

    for i in range(0, len(sentence_list)):
        if sent_score_list[i]==max_score_value:
            candidate_list.append((sentence_list[i],i))
    #print 'Candidate list is :',candidate_list

    if len(candidate_list)==1:
        q_plist,q_olist,q_llist,q_tlist,q_proflist=NET.named_entity_tagging(stop_words_free_question)
        #If the question has a profession but not name of person, then the answer sentence should/would most probably
        #the name of a person
        #print 'Question Person List',q_plist

        if q_plist == [] or q_proflist != []:
            #temp_result=master_person_list[candidate_list[0][1]][0]
            s_plist,s_olist,s_llist,s_tlist,s_proflist=NET.named_entity_tagging(candidate_list[0][0])
            result= ' '.join(s_plist)
            print 'Answer: ',result+'\n'
            #print '\n'
            return result

        elif q_plist != [] or q_proflist != []:
            #print candidate_list[0][1]
            s_plist,s_olist,s_llist,s_tlist,s_proflist=NET.named_entity_tagging(candidate_list[0][0])
            result= ' '.join(s_plist)
            print 'Answer: ',result+'\n'
            #print '\n'
            return result

        elif q_plist != [] or q_proflist == []:  # Implies question has a name. So pick a sentence which has the same name in sentence which is present in question #
            result=candidate_list[0][0]
            print 'Answer: ',result+'\n'
            #print '\n'
            return result
    else:
        # There are more than one candidate sentences. Print the first sentence
        for k in range(0, len(candidate_list)):
            val=candidate_list[k][0]
            #print 'val is :',val
            index=candidate_list[k][1]
            #print 'index is :', index
            temp_list.append(index)
            break

        #result=' '.join(temp_list)
        x= master_person_list[temp_list[0]]
        #print 'x is :', x
        result2 = temp_list[0]
        #for i in range(0,len(x)):
        if x != []:
            temp=' '.join(x[0])
            if temp not in stop_words_free_question:
                final_result_set.append(temp)
        else:
            final_result_set.append(val)

        if final_result_set != []:
            print 'Answer: ',' '.join(final_result_set)+'\n'
            #print '\n'
            #print 'Result 2 is :',result2
            return ' '.join(final_result_set)
        else:
            print 'Answer: ',temp+'\n'
            #print '\n'
            return temp #' '.join(x)


    # Checking to see if the question contains profession name. If so the answer should be a sentence containing a name and higher weights
    # is given for the score from Rule 2. Else Rule 1 and Rule 2 are given equal weightage.

    '''q_plist,q_olist,q_llist,q_tlist,q_proflist=NET.named_entity_tagging(stop_words_free_question)

    #print 'q_proflist',q_proflist

    if q_proflist !=[]:

         ##### score =0.5 * name_score + 0.16667 * WordMatch score + 0.16667 * contains "name" score + 0.16667 * contains "person or name" score

        for i in range(0,len(sentence_list)):
            final_score=0.5 * sent_containing_person_score_list[i] + 0.25*wordmatch_score_list[i] + 0.125*sent_containing_name_score_list[i] + 0.125 * sent_containing_person_or_name_score_list[i]
            candidate_list.append(final_score)

        max_val= max(candidate_list)
        sent_indices_list=[i for i, j in enumerate(candidate_list) if j == max_val]
        if len(sent_indices_list) == 1:
            result_sentence=sentence_list[sent_indices_list[0]]
            master_result_list=master_person_list[sent_indices_list[0]]
            #print master_result_list
            #print q_proflist
            for item in master_result_list:
                if item.lower() not in q_proflist and item not in  stop_words_free_question:
                    final_result_set.append(item)
            #final_result_set = [item for item in master_result_list if item not in q_proflist]
            #print 'index is :',final_result_set
            print 'Final Result is :', ' '.join(final_result_set)
            return ' '.join(final_result_set)

        else:

            for i in range(0,len(sent_indices_list)):
                 master_result_list=master_person_list[sent_indices_list[i]]
                 for item in master_result_list:
                    if item.lower() not in q_proflist and item not in  stop_words_free_question:
                        final_result_set.append(item)

            print 'Final Result is :', ' '.join(final_result_set)
            return ' '.join(final_result_set)
    else:

        # Question does not contain profession, so equal weightage to both 1 and 2.

        ##### score =0.375 * name_score + 0.375 * WordMatch score + 0.125 * contains "name" score + 0.125 * contains "person or name" score

        for i in range(0,len(sentence_list)):
            final_score=0.375 * sent_containing_person_score_list[i] + 0.375*wordmatch_score_list[i] + 0.125*sent_containing_name_score_list[i] + 0.125 * sent_containing_person_or_name_score_list[i]
            candidate_list.append(final_score)

        max_val= max(candidate_list)
        sent_indices_list=[i for i, j in enumerate(candidate_list) if j == max_val]

        #print 'length of list:', len(sent_indices_list)
        if len(sent_indices_list) == 1:
            result_sentence=sentence_list[sent_indices_list[0]]
            master_result_list=master_person_list[sent_indices_list[0]]
            #print 'Final Result is :', result_sentence
            print 'Final Result is :', ' '.join(master_result_list)
            return ' '.join(master_result_list)


        else:
            final_sent_string=""
            for j in range(0,len(sent_indices_list)):
                final_sent_string = sentence_list[sent_indices_list[j]]
                master_result_list=master_person_list[sent_indices_list[j]]
                break


            ## TODO LOOK OUT FOR THE NAMES IN THE FINAL_SENT_STRING AND PRINT THEM ALONE IN ANSWER

            for item in master_result_list:
                if item.lower() not in q_proflist and item not in  stop_words_free_question:
                    final_result_set.append(item)
            #final_result_set = [item for item in master_result_list if item not in q_proflist]
            #print 'index is :',final_result_set
            print 'Final Result is :', ' '.join(final_result_set)
            return ' '.join(final_result_set)

            #print 'Final Result is :', final_sent_string
            #return final_sent_string'''
