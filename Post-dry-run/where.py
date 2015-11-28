__author__ = 'Anirudh'

import WM
import NET
import nltk
import POS_Tagging
from nltk.stem.wordnet import WordNetLemmatizer
nltk.data.path.append("/home/anirudhn/nltk_data")

# The selection of answer is based on the sentence which gets the maximum total score across the four conditions ##

# But generally answers to "when" questions almost always involves a time expression, so sentences that do not contain a time
# expression are only considered in special cases

def answering_where(cleansedQuestion,stop_words_free_question,complete_sentence_list,sentence_list,dateline,sent_loc_list):

    # Declaring globals to be used in this function

    candidate_list=[]
    sent_score_list=[]
    q_verblist=[]

    stanford_stop_words_list=['a','an','and','are','as','at','be','buy','for','from',
                          'has','he','in','is','it','its','of','on','that','the',
                          'to','was','were','will','with']



    location_prepositions=['above','across','after','against','along','among','around',
                           'before','behind','below','beneath','beside','between','by','down','from',
                           'in','inside','into','near','off','onto','opposite','outside','over','surrounding',
                           'round','through','towards','under','up']

    '''in','at','near','inside','on','behind','above','under','next','below','between','around',
                           'outside','among', 'across','front','opposite','before','beneath','beside','against']'''


    temp_q=cleansedQuestion
    temp_q=temp_q.replace('"','')
    temp_q=temp_q.replace("'",'"')
    temp_q=temp_q.replace('?','')

    print 'Question is :',temp_q

    pos_list= POS_Tagging.pos_tagging(temp_q)

    for i in range(0, len(pos_list)):
        if pos_list[i][1] in ['VB','VBD','VBZ','VBN'] and pos_list[i][0] not in stanford_stop_words_list:
            q_verblist.append(pos_list[i][0])

    print 'Question verb list is :',q_verblist
    print 'Master location list is:',sent_loc_list
    # 1. Find score for each sentence using word march score first

    for i in range(0,len(sentence_list)):
        score=0

        print 'Sentence is :',sentence_list[i]
        #score= score + WM.stemWordMatch(cleansedQuestion,sentence_list[i])
        score= score + WM.stemWordMatch(stop_words_free_question,sentence_list[i])
        #print 'After wordmatch score is:',score

        #2. Check if the sentence contains location preposition, then it is a good clue

        for k in complete_sentence_list[i].split():
            if k in location_prepositions:
                score=score+4
        #print 'After location prepostion score is',score

        # 3. Check if the sentence contains Location entity

        if sent_loc_list[i] != []: # If sentence contains location
            score=score + 6

        #print 'After location  score is',score
        # 4.  Reward sentences which has the verb appearing in the question in its sentence

        # 4.  Reward sentences which has "from" in the question and in the answer too

        from_qflag=0
        cand_list=[]

        for k in temp_q.split():
            if k.lower()=='from':
                #print 'From qflag is true'
                from_qflag=1
        if from_qflag==1 and 'from' in complete_sentence_list[i]:
            print 'True:'
            if sent_loc_list[i] !=[]:
                for m in sent_loc_list[i]:
                    if m not in temp_q:
                        cand_list.append(m)
            if cand_list!=[]:
                return ' '.join(cand_list)
            else:
                for k in complete_sentence_list[i].split():
                    if k not in temp_q:
                        cand_list.append(k)
                return ' '.join(cand_list)

        '''sent_pos_list=POS_Tagging.pos_tagging(complete_sentence_list[i])
        lmtzr=WordNetLemmatizer()
        for k in range(0, len(sent_pos_list)):
            if sent_pos_list[k][1] in ['VB','VBD','VBZ','VBN'] and lmtzr.lemmatize(sent_pos_list[k][0]) in q_verblist:
                print 'Verb in question and sentence matches'
                score=score + 6'''

        sent_score_list.append(score)

    print 'Sent score list is :', sent_score_list

    ##################### COMPUTING THE DATE LINE SCORE FOR THE QUESTION #####################

    # For when and where questions the answer to the question could also be from the timeline of the story

    dateline_score=0
    first_sentence_flag=0
    temp_list=cleansedQuestion.split()

    flag=0
    for word in temp_list:
        if word.lower() == 'where':
            flag=1


    for i in range(0, len(temp_list)):
        # 1. If question contains "happen", it is a good clue that timeline could be answer
        if temp_list[i].lower()=='happen':
            dateline_score= dateline_score+4

        # 2. If question contains "take place", it is a good clue that timeline could be answer
        if i != len(temp_list)-1 and temp_list[i].lower()=='take' and temp_list[i+1].lower()=='place':
            dateline_score=dateline_score+4

        # 3. If question contains "this", it is slam_dunk that timeline could be answer for when type questions
        if temp_list[i].lower()=='this':
            if flag==0:
                dateline_score= dateline_score+20
            else:
                first_sentence_flag=1

        # 4. If question contains "story", it is slam_dunk that timeline could be answer

        if temp_list[i].lower()=='story' and flag==0:
            dateline_score= dateline_score+20

    print 'Date line score for the question is :',dateline_score

    first_list=[]

    if first_sentence_flag==1:                        #Choose the first sentence as the answer
        pos_np_list=POS_Tagging.pos_NNP_tagging(complete_sentence_list[0])
        if pos_np_list !=[]:
            for k in pos_np_list:
                if k not in temp_q:
                    first_list.append(k)

            return ' '.join(first_list)
        else:
            return complete_sentence_list[0]

    # Selecting the sentence/sentences that has the maximum score.

    max_score_value =max(sent_score_list)

    #Creating candidate list of sentences based on the maximum sent score

    for i in range(0, len(sentence_list)):
        if sent_score_list[i] == max_score_value:
            candidate_list.append((complete_sentence_list[i],i))


    print 'Candidate list is :',candidate_list

    # Checking which of the scores is greater. IF score from sent_Score_list is greater than dateline score, then we find
    # the corresponding sentences and choose the best among them. Else we return the dateline as the result.
    if max_score_value > dateline_score:

    # Now we have to choose the best sentence among the sentences in candidate list

        if len(candidate_list)==1:

            temp_str= candidate_list[0][0]
            index=candidate_list[0][1]

            #Cleaning up the candidate sentence
            # Replacing double quotes with blank and single quotes with "
            temp_str=temp_str.replace('"','')
            temp_str=temp_str.replace("'",'"')
            temp_str=temp_str.replace(',','').replace('?','').replace('!','')

        # If there are multiple candidates, then choose the sentence which appeared first in the story and then do the processing
        else:
            # There are more than one candidate sentences. Print the first sentence
            for k in range(0, len(candidate_list)):

                temp_str=candidate_list[k][0]
                index=candidate_list[k][1]

                #Cleaning up the candidate sentence

                temp_str=temp_str.replace('"','')
                temp_str=temp_str.replace("'",'"')
                temp_str=temp_str.replace(',','').replace('?','').replace('!','')

                break

        ################### SENTENCE PROCESSING #######################

        result_list=[]
        answer_list=[]

        s_loclist=sent_loc_list[index]

        print 'Location list:', s_loclist


        if s_loclist==[]:   #The selected sentence does not seem to have a location expression, then print whole sentence  minus the words in the question
            '''nnp_list = POS_Tagging.pos_NNP_tagging(temp_str)
            if nnp_list != []:
                for k in nnp_list:
                    if k not in temp_q:
                        result_list.append(k)
                if result_list !=[]:
                    return ' '.join(result_list)'''

            for k in temp_str.split():
                if k not in temp_q:
                    result_list.append(k)
                if result_list !=[]:
                    return ' '.join(result_list)


        if s_loclist!=[]:
            for i in range(0, len(s_loclist)):
                if s_loclist[i] not in temp_q :   #To counter situations where question has a location and NER doesn't identify it
                    answer_list.append(s_loclist[i])

        print 'Answer list is :',answer_list

        temp_result=[]
        np_result_list=[]

        if answer_list != []:
           result=' '.join(answer_list)
           return result

        else:

            np_list = POS_Tagging.pos_noun_tagging(temp_str)
            if np_list != []:
                for k in np_list:
                    if k not in temp_q:
                        np_result_list.append(k)

                return ' '.join(np_result_list)



            '''for k in temp_str.split():
                if k not in temp_q:
                    temp_result.append(k)

            return ' '.join(temp_result)'''

    # Dateline score is greater than the sent list score
    else:
        result=dateline
        return result


