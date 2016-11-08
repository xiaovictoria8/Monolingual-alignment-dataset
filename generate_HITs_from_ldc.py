import csv
import sys
import Queue
import nltk

import hits_classes as hits
import util_functions as util

def top_pairs_by_jaccard_distance(n, ldc_file, max_val = None):
    """
    Args:
        n : The number of sentence pairs to return
        ldc_file : The filename of the LDC CSV dataset
        max_val : The maximum jaccard distance that any returned sentence pair will possess
                  If max_val == None, then there is no max limit
        
    Returns:
        A list of the top n sentence pairs in ldc_file, as sorted by jaccard distance.
        Each sentence pair is represented as a HITUnalignedInput
        All sentence pairs must have a jaccard distance strictly less than max_val
    """
    return top_pairs_by_function(n, ldc_file, util.get_jaccard_dist, max_val)

def top_pairs_by_length_difference(n, ldc_file, max_val):
    """
    Args:
        n : The number of sentence pairs to return
        ldc_file : The filename of the LDC CSV dataset
        max_val : The maximum length difference that any returned sentence pair will possess
                  If max_val == None, then there is no max limit
        
    Returns:
        A list of the top n sentence pairs in ldc_file, as sorted by length difference.
        Each sentence pair is represented as a HITUnalignedInput
        All sentence pairs must have a length difference strictly less than max_val
    """
    return top_pairs_by_function(n, ldc_file, util.get_length_difference, max_val)
    
def top_pairs_by_function(n, ldc_file, f, max_val = None):
    """
    Args:
        n : The number of sentence pairs to return
        ldc_file : The filename of the LDC CSV dataset
        f : A function that takes in two tokenized sentence pairs (strings) and returns an int value. 
            Ldc will be sorted by this function
        max_val : The maximum jaccard distance that any returned sentence pair will possess
                  If max_val == None, then there is no max limit
        
    Returns:
        A list of the top n sentence pairs in ldc_file, as sorted by the function f.
        Each sentence pair is represented as a HITUnalignedInput.
        All sentence pairs must have a jaccard distance strictly less than max_val
    """
    pq = Queue.PriorityQueue(); # queue of the top n sentence pairs encountered so far
    
    # open data file
    ldc = csv.reader(open(sys.argv[1], 'rb'), delimiter = '\t', quotechar=None)
    
    for row in ldc:
        pair_count = -1
        
        # scan through all possible sentence pairs in each row of the ldc
        for i in range(8, len(row)):
            for j in range(i + 1, len(row)):
                pair_count += 1
                src_token = nltk.word_tokenize(row[i])
                tgt_token = nltk.word_tokenize(row[j])
                
        # only select sentences that have between 5 and 30 words and end in punctuation
        if (len(tgt_token) < 30 and len(tgt_token) > 5 and 
                        len(src_token) < 30 and len(src_token) > 5
                        and not row[i][0].islower() and not row[j][0].islower()
                        and row[i][len(row[i]) - 1] in "!\".?"
                        and row[j][len(row[j]) - 1] in "!\".?"):
            
            # create the appriopriate HIT representation for the sentence pairs
            pair_id = row[2] + "-" + row[3] + "-" + str(pair_count)
            src = ' '.join(src_token)
            tgt = ' '.join(tgt_token)
            src_lemma = util.get_lemmatized_version(row[i])
            tgt_lemma = util.get_lemmatized_version(row[j])
            
            f_val = f(src_lemma, tgt_lemma)
            
            # ignore if jaccard distance exceed max_val
            if f_val >= max_val:
                continue
            
            # create new HITUnalignedInput object
            hit = hits.HITUnalignedInput(
                    pair_id = pair_id,
                    doc_id = row[2],
                    segment_id = row[3],
                    source = src,
                    target = tgt
                )
            
            # insert pair into heap and then discard min 
            if pq.qsize() < n:
                pq.put((f_val, hit));
            elif f_val > pq.queue[0][0]:
                pq.get()
                pq.put((f_val, hit))
            
    # reconstruct and return list of HITs
    ret_list = []
    while pq.qsize() > 0:
        ret_list.append(pq.get()[1])
        return ret_list[::-1]

    
def align_list_of_hits(l):
    """
    Uses Sultan's monolingual aligner to produce initial alignments for a list of HITUnalignedInput.
    Args:
        l : The list of sentence pairs that will be converted to a list of HITInput objects.
            Each sentence pair is represented as a HITUnalignedInput.
        
    Returns:
        A list of the sentence pairs in l, with each sentence pair represented as a HITInput object.
    """
    

