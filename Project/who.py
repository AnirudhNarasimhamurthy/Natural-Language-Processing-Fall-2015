__author__ = 'Anirudh'

import WM
import NET

# The selection of answer is based on the sentence which gets the maximum total score across the four conditions ##

# But generally answers to "who" questions involve a person and so the maximum priority is given to them than other sentences


def answering_who(question,cleansedQuestion,stop_words_free_question,sentence_list):

    # Declaring globals to be used in this function

    wordmatch_score_list=[]
    sent_containing_person_score_list=[]
    sent_containing_name_score_list=[]
    sent_containing_person_and_name_score_list=[]
    sent_containing_person_or_name_score_list=[]
    master_person_list=[]

    print 'Question is :',cleansedQuestion

    # 1. Score using word match rule

    for i in range(0, len(sentence_list)):
        #print 'Sentence is :', sentence_list[i]
        wordmatch_score_list.append(WM.stemWordMatch(cleansedQuestion,sentence_list[i]))


    print 'After 1, scores are :',wordmatch_score_list

    # 2. If question does not contain name but the answer contains NAME then you are confident(+6)
    # 3. If question does not contain a name and answer contains the word "name" then good_clue (+4)

    # Checking if the question has a name or not

    q_person_list,org_list,loc_list,prof_list = NET.named_entity_tagging(cleansedQuestion)

    print 'person list in question is :',q_person_list

    if q_person_list==[]:
        #Checking if the sentences have a name or person entity in them
        for i in range(0, len(sentence_list)):
            sent_plist,sent_olist,sent_llist,sent_proflist=NET.named_entity_tagging(sentence_list[i])
            master_person_list.append(sent_plist)
            if sent_plist !=[]:
                count=0
                for j in range(0, len(sent_plist)):
                    if j==0:
                        count=count+6
                        #print sent_containing_person_score_list[0][0]
                    else:
                        count=count+6
                sent_containing_person_score_list.append(count)
            else:
                sent_containing_person_score_list.append(0)

            if sent_plist==[] and "name" in sentence_list[i]:
                sent_containing_name_score_list.append(4)
            else:
                sent_containing_name_score_list.append(0)
    else:
        #Question has a name, so tha answer should definitely be a Person/Name
        for i in range(0, len(sentence_list)):
            sent_plist,sent_olist,sent_llist,sent_proflist=NET.named_entity_tagging(sentence_list[i])
            master_person_list.append(sent_plist)
            if sent_plist !=[]:
                count=0
                for j in range(0, len(sent_plist)):
                    if j==0:
                        count=count+6
                        #print sent_containing_person_score_list[0][0]
                    else:
                        count=count+6
                sent_containing_person_score_list.append(count)
            else:
                sent_containing_person_score_list.append(0)

            if sent_plist==[] and "name" in sentence_list[i]:
                sent_containing_name_score_list.append(4)
            else:
                sent_containing_name_score_list.append(0)


    print 'After 2 and 3, scores are :',sent_containing_person_score_list,sent_containing_name_score_list

    #  4. Awards points to all sentences  that contain a name or reference to a human
    for i in range(0, len(sentence_list)):
            sent_plist,sent_olist,sent_llist,sent_proflist=NET.named_entity_tagging(sentence_list[i])
            #print 'Profession list is :', sent_proflist
            if sent_plist != [] and sent_proflist !=[]:
               sent_containing_person_and_name_score_list.append(12)
            else:
                sent_containing_person_and_name_score_list.append(0)

            if sent_plist !=[] or sent_proflist != []:
               sent_containing_person_or_name_score_list.append(4)
            else:
                sent_containing_person_or_name_score_list.append(0)

    print 'After 4 name and person list is :', sent_containing_person_and_name_score_list
    print 'After 4 name or person list is :', sent_containing_person_or_name_score_list

    # Selecting the sentence that has the maximum score. If it is a tie, we choose the sentence that appears first
    # Preference is given to sentences which have a person name in them. If there is only one such sentence that is the answer
    #If there are multiple such sentences then score is computed by the following logic:

    ##### score =0.5 * name_score + 0.16667 * WordMatch score + 0.16667 * contains "name" score + 0.16667 * contains "person or name" score

    candidate_list=[]
    final_result_set=[]
    pandname_list=[]

    '''if  len(sent_containing_person_score_list)== 1:
        result=sentence_list[sent_containing_person_score_list[0][1]]
        print 'Result is :', result'''


    '''for i in range(0, len(sent_containing_person_and_name_score_list)):
            if sent_containing_person_and_name_score_list[i] > 0:
                pandname_list.append(sentence_list[i])

    print 'pand name:',pandname_list'''
    # Parse the question to see if it has any indicators to the answer

    q_plist,q_olist,q_llist,q_proflist=NET.named_entity_tagging(stop_words_free_question)

    print 'q_proflist',q_proflist

    if q_proflist !=[]:


        for i in range(0,len(sentence_list)):
            final_score=0.5 * sent_containing_person_score_list[i] + 0.25*wordmatch_score_list[i] + 0.125*sent_containing_name_score_list[i] + 0.125 * sent_containing_person_or_name_score_list[i]
            candidate_list.append(final_score)

        max_val= max(candidate_list)
        sent_indices_list=[i for i, j in enumerate(candidate_list) if j == max_val]
        if len(sent_indices_list) == 1:
            result_sentence=sentence_list[sent_indices_list[0]]
            master_result_list=master_person_list[sent_indices_list[0]]
            print master_result_list
            #print q_proflist
            for item in master_result_list:
                if item.lower() not in q_proflist and item not in  stop_words_free_question:
                    #print item.lower()
                    #print q_proflist
                    final_result_set.append(item)
            #final_result_set = [item for item in master_result_list if item not in q_proflist]
            #print 'index is :',final_result_set
            print 'Final Result is :', final_result_set
            return final_result_set
    else:

        print 'Here:'
        for i in range(0,len(sentence_list)):
            final_score=0.375 * sent_containing_person_score_list[i] + 0.375*wordmatch_score_list[i] + 0.125*sent_containing_name_score_list[i] + 0.125 * sent_containing_person_or_name_score_list[i]
            candidate_list.append(final_score)

        max_val= max(candidate_list)
        sent_indices_list=[i for i, j in enumerate(candidate_list) if j == max_val]

        print 'length of list:', len(sent_indices_list)
        if len(sent_indices_list) == 1:
            result_sentence=sentence_list[sent_indices_list[0]]
            '''master_result_list=master_person_list[sent_indices_list[0]]
            print master_result_list
            for item in master_result_list:
                if item.lower() not in q_proflist:
                    print item.lower()
                    print q_proflist
                    final_result_set.append(item)'''
            print 'Final Result is :', result_sentence
            return result_sentence


        else:
            final_sent_string=""
            for j in range(0,len(sent_indices_list)):
                final_sent_string = sentence_list[sent_indices_list[j]]
                break

            print 'Final Result is :', final_sent_string
            return final_sent_string
    # If there are multiple sentences in the list, then we have to choose the most appropriate one


    #print 'Result sentence is :', sentence_list[sentence_score_list.index(max(sentence_score_list))]
    #print 'Max value is :', max(sentence_score_list)