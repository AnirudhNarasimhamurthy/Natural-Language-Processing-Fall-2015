__author__ = 'Anirudh'

import nltk
import re

'''
stopwords_free_sentences_list=['A middle school in Liverpool, Nova Scotia is pumping up bodies as well as minds.', 'It''s an example of a school teaming up with the community to raise money.'
        ,'South Queens Junior High School is taking aim at the fitness market','Principal Betty Jean Aucoin says the club is a first for a Nova Scotia public school.']
'''

def named_entity_tagging(stopwords_free_sentences_list):

    final_person_list=[]
    final_org_list=[]
    final_loc_list=[]

    for i in range(0, len(stopwords_free_sentences_list)):
        tokens = nltk.word_tokenize(stopwords_free_sentences_list[i])
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)
        #print 'Entities in sentences are :', entities
        #print type(entities)
        count=0
        ent_list=[]
        for i in range(0, len(entities)):
            ent_list.append(str(entities[i]))

        #print ent_list

        person_name_list=[]
        org_name_list=[]
        loc_name_list=[]
        temp_list=[]
        p_start = 8
        o_start=14
        l_start=5
        s=""
        for i in range(0, len(ent_list)):
                if 'PERSON' in ent_list[i]:
                    #print 'ent_list[i]', ent_list[i]
                    person_index_list = [m.start() for m in re.finditer('/NNP', ent_list[i])]
                    #print 'Person index list is :', person_index_list
                    if len(person_index_list) == 1:
                        #print 'single person'
                        person_name_list.append(ent_list[i][p_start:person_index_list[0]])
                        #print 'person:',person_name_list
                        #continue
                    elif len(person_index_list) > 1:
                        for j in range(0, len(person_index_list)):
                            temp_list.append(ent_list[i][p_start:person_index_list[j]])
                            #print temp_list
                            p_start=person_index_list[j]+5
                            #print person_name_list
                        t=' '.join(temp_list)
                        p_start=8
                        temp_list=[]
                        person_name_list.append(t)


                elif 'ORGANIZATION' in ent_list[i]:
                    #print 'ent_list[i]', ent_list[i]
                    org_index_list = [m.start() for m in re.finditer('/NNP', ent_list[i])]
                    #print 'org index list is :', org_index_list
                    if len(org_index_list) == 1:
                        #print 'single org'
                        org_name_list.append(ent_list[i][o_start:org_index_list[0]])
                        #print 'org:',org_name_list
                        #continue
                    elif len(org_index_list) > 1:
                        for j in range(0, len(org_index_list)):
                            temp_list.append(ent_list[i][o_start:org_index_list[j]])
                            #print temp_list
                            o_start=org_index_list[j]+5
                            #print person_name_list
                        t=' '.join(temp_list)
                        o_start=14
                        temp_list=[]
                        org_name_list.append(t)


                elif 'GPE' in ent_list[i]:
                    #print 'ent_list[i]', ent_list[i]
                    loc_index_list = [m.start() for m in re.finditer('/NNP', ent_list[i])]
                    #print 'loc index list is :', loc_index_list
                    if len(loc_index_list) == 1:
                        #print 'single loc'
                        loc_name_list.append(ent_list[i][l_start:loc_index_list[0]])
                        #print 'loc:',loc_name_list
                        #continue
                    elif len(loc_index_list) > 1:
                        for j in range(0, len(loc_index_list)):
                            temp_list.append(ent_list[i][l_start:loc_index_list[j]])
                            #print temp_list
                            l_start=loc_index_list[j]+5
                            #print person_name_list
                        t=' '.join(temp_list)
                        l_start=5
                        temp_list=[]
                        loc_name_list.append(t)


        final_person_list.append(person_name_list)
        final_org_list.append(org_name_list)
        final_loc_list.append(loc_name_list)


    print 'Person name list is :',final_person_list
    print 'Org name list is :',final_org_list
    print 'Loc name list is :',final_loc_list


    return final_person_list,final_org_list,final_loc_list

