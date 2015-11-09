__author__ = 'Anirudh'


# Takes a list containing all the questions from the question file and returns two lists containing the questionID and the question #

def question_parser(question_list):

    questionID_list=[]
    q_list=[]
    '''print len(question_list)
    for i in range(0, len(question_list)):
        print i, question_list[i]'''
    for i in range(0, len(question_list)):
        if i%4==0:
            questionID_list.append(question_list[i])
        elif i%4==1:
            q_list.append(question_list[i])

    return questionID_list,q_list