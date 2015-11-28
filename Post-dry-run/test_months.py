__author__ = 'Anirudh'
import NER
sentence_list=['This is January','She flew in December','In March he got a $50 ticket -- and decided to take it to court']
for i in sentence_list:
    NER.named_entity_recognition(i)