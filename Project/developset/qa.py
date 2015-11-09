__author__ = 'Anirudh'


import sys

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

print 'Data is :', data


######################## Getting the question and story from the given input story ID ##############################

directory_path=data[0]
print 'Directory path is :', directory_path

#######################  Computing the full directory path for story and question from storyID #######################

for i in range(1, len(data)):
    story_id=data[i]
    question_path=directory_path + '/' + story_id + '.questions'
    story_path=directory_path + '/' + story_id + '.story'
    print 'Question file is :', question_path
    print 'Story file is :', story_path

    ################## Reading the corresponding story and the questions for the given story id ###################
    with open(story_path, 'r') as storyFile:
        story=storyFile.readlines()