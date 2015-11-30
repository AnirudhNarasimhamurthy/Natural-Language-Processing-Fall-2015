__author__ = 'Anirudh'
import WM
import nltk
nltk.data.path.append("/home/anirudhn/nltk_data")


def answering_which(cleansedQuestion,stop_words_free_question,complete_sentence_list,sentence_list):


    # Declaring globals to be used in this function

    candidate_sent_list=[]
    sent_score_list=[]

    for i in range(0,len(complete_sentence_list)):
        score=0

        # 1. Find score for each sentence using word march score first

        #print 'The sentence is :',complete_sentence_list[i]
        #score = score + WM.stemWordMatch(cleansedQuestion,sentence_list[i])
        score = score + WM.stemWordMatch(stop_words_free_question,sentence_list[i])

        sent_score_list.append(score)

    #print 'Score list is:',sent_score_list
    max_score_value=max(sent_score_list)

    # Finding the sentences which has the highest score and adding them to the best list


    final_sent_list=[]
    temp_result=[]

    for i in range(0,len(sentence_list)):
        if sent_score_list[i]==max_score_value:
            final_sent_list.append(complete_sentence_list[i])

    #print 'Final sent list is:',final_sent_list


    if len(final_sent_list) == 1:
        temp = final_sent_list[0].split()
        for k in range(0, len(temp)):
            if temp[k].lower()=='that':
                return ' '.join(temp[k:])

        return final_sent_list[0]
    else:
        for k in range(0,len(final_sent_list)):
            result=final_sent_list[k]
            break

        temp = result.split()
        for k in range(0, len(temp)):
            if temp[k].lower()=='that':
                return ' '.join(temp[k:])

        return result
