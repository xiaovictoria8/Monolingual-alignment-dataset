import nltk.stem.wordnet as wn
import nltk
import re

""" Returns Jaccard distance of two string inputs """
def get_jaccard_dist(target_sent, source_sent):
    
    # tokenize and tag both strings
    target_words = nltk.pos_tag(nltk.word_tokenize(target_sent.lower()))
    source_words = nltk.pos_tag(nltk.word_tokenize(source_sent.lower()))
    
    # convert Treebank POS tags to WordNet tags
    target_words = [(tag[0], get_wordnet_tag(tag[1])) for tag in target_words]
    source_words = [(tag[0], get_wordnet_tag(tag[1])) for tag in source_words]
    
    # lemmatize all words
    lmtzr = wn.WordNetLemmatizer()
    target_words = [lmtzr.lemmatize(tag[0], tag[1]) for tag in target_words]
    source_words = [lmtzr.lemmatize(tag[0], tag[1]) for tag in source_words]
    
    #convert to set and calculate jaccard dist
    target_set = set(target_words)
    source_set = set(source_words)
    
    intersection = len(target_set & source_set)
    union = len(target_set | source_set)
    if union != 0:
      return 1.0 - float(intersection)/union
    else:
      return 1

"""Converts a Penn Treebank part-of-speech tag to a WordNet part-of-speech tag"""
def get_wordnet_tag(treebank_tag):
    chartype = treebank_tag[0]
    if chartype == 'J': # adjective
        return 'a'
    elif chartype == 'V': # verb
        return 'v'
    elif chartype == 'R': # adverb
        return 'r'
    else: # nouns and other parts of speech
        return 'n'
    

"""Takes in set of sure alignments a_sure and all control alignments b_all and returns the precision of a"""
def precision(a_sure, b_all):
    if len(a_sure) == 0:
        return 0
    intersect_len = len(a_sure & b_all)
    return float(intersect_len) / len(a_sure)
    
"""Takes in a set of all alignments a_all and sure control alignments b_sure and returns the recall of a"""
def recall(a_all, b_sure):
    intersect_len = len (a_all & b_sure)
    return float(intersect_len) / len(b_sure)

""" Takes in the recall and precision values, returns F1 calculation """
def f1(prec, rec):
    if prec == 0 or rec == 0:
        return 0
    return float(2 * prec * rec) / float(prec + rec)
    
"""NOTE: The following functions only consider "sure" alignments for their calculations."""
""" Takes in the set of submitted alignments (sub) and set of correct answers (ans), returns precision calculation """
def precision_sure_only(sub, ans):
    if len(sub) == 0:
        return 0
    intersect_len = len(sub & ans)
    return float(intersect_len) / len(sub)

""" Takes in the set of submitted alignments (sub) and set of correct answers (ans), returns recall calculation """
def recall_sure_only(sub, ans):
    intersect_len = len(sub & ans)
    return float(intersect_len) / len(ans)
