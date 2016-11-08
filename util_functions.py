import nltk.stem.wordnet as wn
import nltk
import re

""" Returns Jaccard distance of two string inputs """
def get_jaccard_dist(src, tgt):
    # convert input sentences into sets of words
    source_set = set(src.split())
    target_set = set(tgt.split())
    
    #convert to set and calculate jaccard dist
    intersection = len(target_set & source_set)
    union = len(target_set | source_set)
    
    if union != 0:
      return 1.0 - float(intersection)/union
    else:
      return 1
  
""" Returns length difference of two string inputs """
def get_length_difference(src, tgt):
    src_list = src.split()
    tgt_list = tgt.split()
    return abs(len(src_list) - len(tgt_list))
    

"""Returns a lowercased, tokenized and lemmatized version of string s"""
def get_lemmatized_version(s):
    # tokenize, lowercase and tag string
    s_list = nltk.pos_tag(nltk.word_tokenize(s.lower()))
    
    # convert Treebank POS tags to WordNet tags
    lmtzr = wn.WordNetLemmatizer()
    s_list = [lmtzr.lemmatize(tag[0], get_wordnet_tag(tag[1])) for tag in s_list]
    
    # return a string with spaces between each token
    return " ".join(s_list)


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
    print "prec", prec
    print "rec", rec
    print "float(2 * prec * rec) ", float(2 * prec * rec) 
    print "float(prec + rec)", float(prec + rec)
    print "f1", float(2 * prec * rec) / float(prec + rec)
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