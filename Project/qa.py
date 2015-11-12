__author__ = 'Anirudh'


import sys
import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import NERTagger
import QP
import WM
import NET
import who
import when
import where
import what
import why


from time import gmtime, strftime


################ Getting the input file from the command line arguments ###########################

if len(sys.argv) > 1:
    input_file=sys.argv[1]
else:
    print 'Please provide an input file as an argument to this qa system !'

######################### Reading the input file #########################################

with open(input_file, 'r') as input:
    data=input.readlines()

for i in range(0, len(data)):
    data[i]=data[i].replace("\n","")

#print 'Data is :', data


######################## Getting the question and story from the given input story ID ##############################

directory_path=data[0]
#print 'Directory path is :', directory_path

#######################  Computing the full directory path from the storyID for story and question  #######################

for i in range(1, len(data)):
    story_id=data[i]
    question_path=directory_path + '/' + story_id + '.questions'
    story_path=directory_path + '/' + story_id + '.story'
    #print 'Question file is :', question_path
    #print 'Story file is :', story_path

    ##################   Reading the corresponding story file for the given story id ###################

    with open(story_path, 'r') as storyFile:
        story=storyFile.readlines()

    for i in range(0,len(story)):
        story[i]=story[i].replace("\n","")


    #print 'Story is :', story
    sentences_list,hline_date=QP.story_parser(story)


    #### Removing the stop words from  each sentence using NLTK's stopwords and then creating a final stop word free sentence list ###

    stops = set(stopwords.words('english'))
    stops.remove("this")
    stops.remove("so")

    #print 'Number of stop words in NLTK library is :',len(stops)

    non_stop_words=[]
    stopwords_free_sentences_list=[]
    for sent in sentences_list:
        for w in sent.split():
            if w.lower() not in stops:
                non_stop_words.append(w)
        temp=' '.join(non_stop_words)
        stopwords_free_sentences_list.append(temp)
        non_stop_words=[]

    #print 'After stop words removal the sentences list is:', stopwords_free_sentences_list
    #print len(stopwords_free_sentences_list)



    ################## Reading the corresponding question file for the given story id ###################

    with open(question_path, 'r') as questionFile:
        question=questionFile.readlines()

    for i in range(0,len(question)):
        question[i]=question[i].replace("\n","")

    #print 'Question is :', question

    qIDList, qList,cleansedqList = QP.question_parser(question)

    #print 'QuestionID List is :', qIDList
    #print 'Question list is :', qList
    #print 'Cleansed question list is :',cleansedqList
    #print len(qList)



    ################## Removing the stopwords from each question using NLTK's stopwords list ###################

    non_stop_words=[]
    stopwords_free_questions_list=[]
    for sent in qList:
        for w in sent.split():
            if w.lower() not in stops:
                non_stop_words.append(w)
        temp=' '.join(non_stop_words)
        stopwords_free_questions_list.append(temp)
        non_stop_words=[]




    ################### CATEGORIZING THE QUESTION AS WH0, WHAT, WHEN , WHY , WHERE OR HOW  ########################

    who_list,what_list,when_list,why_list,where_list,how_list=[],[],[],[],[],[]
    answer_list=[]

    for i in range(0, len(cleansedqList)):
        qWords= cleansedqList[i].split()
        print qIDList[i]
        for j in range(0, len(qWords)):
            if qWords[j].lower()=='who':
                #print 'Who question',cleansedqList[i]
                answer_list.append(who.answering_who(cleansedqList[i],stopwords_free_questions_list[i],stopwords_free_sentences_list)) #stopwords_free_sentences_list
                break
            elif qWords[j].lower()=='what':
                #what_list.append(cleansedqList[i])
                answer_list.append(what.answering_what(cleansedqList[i],stopwords_free_questions_list[i],sentences_list,stopwords_free_sentences_list,hline_date)) #stopwords_free_sentences_list
                break
            elif qWords[j].lower()=='when':
                #who_list.append(cleansedqList[i])
                answer_list.append(when.answering_when(cleansedqList[i],stopwords_free_questions_list[i],stopwords_free_sentences_list,hline_date)) #stopwords_free_sentences_list
                break
            elif qWords[j].lower()=='where':
                #where_list.append(cleansedqList[i])
                answer_list.append(where.answering_where(cleansedqList[i],stopwords_free_questions_list[i],sentences_list,stopwords_free_sentences_list,hline_date)) #stopwords_free_sentences_list
                break
            elif qWords[j].lower()=='why':
                #why_list.append(cleansedqList[i])
                answer_list.append(why.answering_why(cleansedqList[i],stopwords_free_questions_list[i],sentences_list,stopwords_free_sentences_list,hline_date)) #stopwords_free_sentences_list
                break
            elif qWords[j].lower()=='how':
                how_list.append(cleansedqList[i])
                break

    '''print 'Questions belonging to who list:', who_list
    print 'Questions belonging to what list:', what_list
    print 'Questions belonging to when list:', when_list
    print 'Questions belonging to where list:', where_list
    print 'Questions belonging to why_list:', why_list
    print 'Questions belonging to how list:', how_list'''


    ##################### HANDLING WHO QUESTIONS #################################





    # Passing the required parameters for the WordMatch function

    response_sent_candidates=[]

    #Calling WordMatch function to compute the number of words that appear in both question and sentence being considered
    '''for i in range(0, len(cleansedqList)):
        for j in range(0, len(stopwords_free_sentences_list)):
            result_count = WM.wordMatch(cleansedqList[i],stopwords_free_sentences_list[j])
            if result_count > 0:
                response_sent_candidates.append(stopwords_free_sentences_list[j])
        #print 'Question is :', cleansedqList[i]
        #print 'Candidate responses are:',response_sent_candidates
        response_sent_candidates=[]'''


    ####### Named  Entity tagging using Stanford NER system for PERSON, ORGANIZATION and LOCATION entities #############
    NER_list=[]

    st = NERTagger('/Users/Anirudh/Desktop/Fall 2015/NLP/Natural-Language-Processing-Fall-2015/Project/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                   '/Users/Anirudh/Desktop/Fall 2015/NLP/Natural-Language-Processing-Fall-2015/Project/stanford-ner-2014-06-16/stanford-ner.jar')


    '''for i in range(0, len(stopwords_free_sentences_list)):
        NER_list.append(st.tag(stopwords_free_sentences_list[i].split()))

    print 'NER List:', NER_list'''

    '''print 'Start time:', strftime("%Y-%m-%d %H:%M:%S", gmtime())

    for i in range(0, len(sentences_list)):
        NER_list.append(st.tag(sentences_list[i].split()))

    print 'End time:',strftime("%Y-%m-%d %H:%M:%S", gmtime())'''

    #print 'NER List:', NER_list


    # Named Entity tagging for the given input sentences

    #person_list, org_list, loc_list = NET.named_entity_tagging(sentences_list)


    # Tokenizing the given questions

    #q_person_list, q_org_list, q_loc_list = NET.named_entity_tagging(cleansedqList)

        #print 'Entities in question are :', entities'''




    ####################### Building the response file #############################################

    with open ("AnswerResponse","w") as f:
	    for i in range(0, len(qIDList)):
                f.write(qIDList[i])
                f.write("\n")
                f.write("Answer: ")
                #f.write(answer_list[i])
                f.write("\n\n")



