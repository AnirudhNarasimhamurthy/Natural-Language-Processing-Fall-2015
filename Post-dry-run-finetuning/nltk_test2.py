__author__ = 'Anirudh'
import nltk

sentences=['A middle school in Liverpool, Nova Scotia is pumping up bodies as well as minds.', 'It''s an example of a school teaming up with the community to raise money.'
        ,'South Queens Junior High School is taking aim at the fitness market','Principal Betty Jean Aucoin says the club is a first for a Nova Scotia public school.']

tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

print chunked_sentences

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        print 'True'
        print t.label
        if t.label == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

entity_names = []
for tree in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)

    entity_names.extend(extract_entity_names(tree))

# Print all entity names
print entity_names

# Print unique entity names
print set(entity_names)

