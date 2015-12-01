__author__ = 'Anirudh'
import re

# Takes a list containing all the questions from the question file and returns three lists
# 1. containing the questionID
# 2. containing the question as is
# 3. containing the cleansed question i.e without the 'Question:'#

def question_parser(question_list):

    questionID_list=[]
    q_list=[]
    '''print len(question_list)
    for i in range(0, len(question_list)):
        print i, question_list[i]'''

    #QuestionID appears first, question appears next the difficulty level and then a newline. This pattern repeats for all questions in questions file #

    for i in range(0, len(question_list)):
        if i%4==0:
            questionID_list.append(question_list[i])
        elif i%4==1:
            q_list.append(question_list[i])


    # Filtering the question list to just contain the question without the word 'Question:'

    cleansedQ_list=[]
    for i in range(0, len(q_list)):
        temp=q_list[i].split()
        temp2 =' '.join(temp[1:])
        cleansedQ_list.append((temp2))

    #print 'Cleansed Q List is :',cleansedQ_list

    return questionID_list,q_list,cleansedQ_list


# Takes a list containing all sentences in a story file and then returns the list of sentences
# constructed as per the '.' and just not the new line #

def story_parser(story):

    story_lines=[]
    story_string=' '.join(story)
    pat = ('(?<!Dr)(?<!Esq)\. +(?=[A-Z])')
    story_lines.append(re.sub(pat,'.\n',story_string))
    #print re.sub(pat,'.\n',story_string)
    #print story_lines



    #The first four lines contain the HEADLINE, DATE and STORY ID and newline
    hd_len=len('HEADLINE: ')
    dt_len=len('DATE: ')
    st_len=len('STORYID: ')
    headline= story[0][hd_len:]
    date=story[1][dt_len:]
    storyID=story[2][st_len:]
    #print 'Headline is :', headline
    #print 'Date of headline is :', date
    #print 'Story Id is :',storyID

    #The next two lines contain the TEXT and newline. SO the actual text content starts from the 7th line of every story file#

    start=5

    #for i in range(start,len(story)):
    story_sents=[]
    fullstop_line=start
    prev_fullstop_index=-1
    #sent_list_index=[]

    #print 'Len of story is :',len(story)

    for i in range(start,len(story)):
        line=""
        if story[i]=='':
            blank_line=i
            continue

        fullstop_index=story[i].find(".")

        # Countering for cases such as .... and i.e and Dr., Mr. and Mrs. and single character like J. Edwards#
        if fullstop_index != -1 and story[i][fullstop_index+1:fullstop_index+2] !='.' and story[i][fullstop_index+1:fullstop_index+2] not in ['e','m'] \
                and story[i][fullstop_index-2:fullstop_index]!='Dr' and story[i][fullstop_index-2:fullstop_index]!='Mr'\
                and story[i][fullstop_index-2:fullstop_index]!='Ms' and not (re.match("^[A-Za-z0-9_-]+$",story[i][fullstop_index+1:fullstop_index+2])):
            min_index=max(blank_line,fullstop_line)
            #print 'Min index is :', min_index

            #If the sentence stretches across two lines starting from a full stop on first line, then include that line also
            #with characters after full stop marking start of the new sentence
            if i-min_index==1 and min_index==fullstop_line:
                line=story[i-1][prev_fullstop_index+1:] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)
            elif i-min_index==1 and min_index==blank_line and story[min_index-1][len(story[min_index-1])-1:len(story[min_index-1])-1]!='.':
                line=story[i-2][prev_fullstop_index+1:]+ " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)

            #If the prev line was a blank line, implies a new line and so just one line
            elif i-min_index==1 and min_index==blank_line:
                line=story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)
            elif i-min_index==2 and min_index==blank_line:
                line=story[i-1]+ " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)

            #If the sentence stretches across three lines starting from a full stop on first line, then include that line also
            #with characters after full stop
            elif i-min_index==2 and min_index==fullstop_line:
                line=story[i-2][prev_fullstop_index+1:] + " "+ story[i-1]+ " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)
            elif i-min_index==3 and min_index==blank_line:
                line=story[i-2]+" "+ story[i-1] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)

            #If the sentence stretches across three lines starting from a full stop on first line, then include that line also
            # with characters after full stop
            elif i-min_index==3 and min_index==fullstop_line:
                line=story[i-3][prev_fullstop_index+1:]+ " " + story[i-2]+" "+ story[i-1] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)


            #IF the sentence stretches across four lines

            elif i-min_index==4 and min_index==blank_line:
                line=story[i-3] + " " +story[i-2]+" "+ story[i-1] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)

            elif i-min_index==4 and min_index==fullstop_line:
                line=story[i-4][prev_fullstop_index+1:]+ " " + story[i-3] + " " +story[i-2]+" "+ story[i-1] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)

            #IF the sentence stretches across five lines

            elif  i-min_index==5 and min_index==blank_line:
                line=story[i-4] + " " + story[i-3] + " " +story[i-2]+" "+ story[i-1] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)

            elif  i-min_index==5 and min_index==fullstop_line:
                line=story[i-5][prev_fullstop_index+1:]+ " " + story[i-4] + " " + story[i-3] + " " +story[i-2]+" "+ story[i-1] + " " + story[i][:fullstop_index+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)


            fullstop_line=i
            prev_fullstop_index=fullstop_index

        sent_list_index= [x for x, v in enumerate(story[i]) if v == '.']

        #print 'sent list index is:',sent_list_index

        if len(sent_list_index) > 1:
            for m in range(1, len(sent_list_index)):
                line=story[i][prev_fullstop_index+1:sent_list_index[m]+1]
                if len(line) < 5:
                    continue
                story_sents.append(line)
                fullstop_line=i
                prev_fullstop_index=sent_list_index[m]

    #print 'Sentences in given story are :', story_sents

    return story_sents,date
