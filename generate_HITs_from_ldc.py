import sys
import Queue
import nltk
import csv
import heapq

import hits_classes as hits
import util_functions as util
import stanford_corenlp_functions as sc
import progress.bar as pgb

def top_pairs_by_function(n, ldc_file, f, max_val = None):
    """
    Args:
        n : The number of sentence pairs to return
        ldc_file : The string filename of the input LDC CSV dataset
        f : A function that takes in two tokenized sentence pairs (strings) and returns an int value. 
            Ldc will be sorted by this function
        max_val : The maximum jaccard distance that any returned sentence pair will possess
                  If max_val == None, then there is no max limit
        
    Returns:
        A list of the top n sentence pairs in ldc_file, as sorted by the function f.
        Each sentence pair is represented as a HITUnalignedInput.
        All sentence pairs must have a f(x) value of strictly less than max_val
    """

    # setup progress bar
    bar = pgb.Bar("Finding top pairs", max = 25495)

    
    pq = Queue.PriorityQueue(); # queue of the top n sentence pairs encountered so far
    
    # open data file
    ldc = csv.reader(open(sys.argv[1], 'rb'), delimiter = '\t', quotechar=None)
    
    for row in ldc:
        bar.next()
        try:
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
                        if max_val and f_val >= max_val:
                            "f_val >= max_val"
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
                            pq.put((f_val, hit))

                        elif f_val > pq.queue[0][0]:
                            pq.get()
                            pq.put((f_val, hit))
                        
        except:
            pass
        
    bar.finish()
             
    # reconstruct and return list of HITs
    ret_list = []
    while pq.qsize() > 0:
#         print "ret_list", ret_list
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
    
    print "starting align_list_of_hits"
    
    # setup bar
    bar = pgb.Bar("Aligning top pairs", max=len(l))
    
    hit_input_list = []
    for unalgn_hit in l:
        bar.next()
        try:
            hit_input = hits.HITInput(
                pair_id = unalgn_hit.pair_id,
                doc_id = unalgn_hit.doc_id,
                segment_id = unalgn_hit.segment_id,
                source = unalgn_hit.source,
                target = unalgn_hit.target,
                sure_align = sc.mono_align(util.get_lemmatized_version(unalgn_hit.source), util.get_lemmatized_version(unalgn_hit.target)),
                poss_align = set(),
                source_hl = set(),
                target_hl = set()
                )
            hit_input_list.append(hit_input)
        except:
            pass
    
    print "done align_list_of_hits"
    print "hit_input_list: ", hit_input_list 
    
    bar.finish()
    
    return hit_input_list


def alignments_to_string(align_set):
    """
    Converts a set of alignments to the alignments format for the Mechanical Turk HITs Input CSV file.
    
    Args:
        alignments : A set of alignments in Pharoah format.
    
    Returns:
        A single string containing a space-seperated list of all alignments in the set.
    """

    return ' '.join([s for s in list(align_set)])
    

def print_hit_input_list_to_csv(l, csv_file):
    """
    Prints a list of HITInput objects to csv_file in the Mechanical Turk HITs Input format.
    Args:
        l : The list of HITInput objects
        csv_file : The string filename of the csv file to print to
    """
    
    # setup bar
    print "starting print_hit_input_list_to_csv"
    bar = pgb.Bar("Printing top pairs", max=len(l))
    
    # open csv writer and print out first row
    print "creating csv_writer"
    csv_writer = csv.writer(open(csv_file, 'w'), delimiter = ',')
    csv_writer.writerow(["pairID", "documentID", "segmentID", "hitType", "source",
                         "target", "sourceLemmatized", "targetLemmatized",
                         "jaccardDistance", "lengthDifference", "sureAlignments", 
                         "possAlignments", "sourceHighlights", "targetHighlights", 
                         "answerSureAlignments", "answerPossAlignments",
                         "answerSourceHighlights", "answerTargetHighlights"])
    
    # print each HITInput object to the CSV file
    print "printing each HITInput object to CSV"
    for hit in l:
        bar.next()
        lemma_src = util.get_lemmatized_version(hit.source)
        lemma_tgt = util.get_lemmatized_version(hit.target)
        csv_writer.writerow([hit.pair_id, hit.doc_id, hit.segment_id, "HITInput", hit.source, 
                             hit.target, lemma_src, lemma_tgt, 
                             util.get_jaccard_dist(lemma_src, lemma_tgt),
                             util.get_length_difference(lemma_src, lemma_tgt), 
                             alignments_to_string(hit.sure_align), alignments_to_string(hit.poss_align), 
                             alignments_to_string(hit.source_hl), alignments_to_string(hit.target_hl), 
                             "", "", "", ""])
    
    print "done"
        
    bar.finish()
    
def main():
    """
    Opens input data file of the LDC corpus and generates a CSV file with the top n sentence pairs 
    given the input metric and upper bound value.
    
    Args:
        sys.argv[1] : the filename of the input LDC corpus CSV file
        sys.argv[2] : the filename of the output CSV file
        sys.argv[3] : n, the number of sentence pairs to generate
        sys.argv[4] : "jd" if rank by jaccard distance, "ld" if rank by length difference 
        sys.argv[5] : the maximum bound in terms of jd/ld to be printed in the output file
    """
    
    max_bound = None if len(sys.argv) <= 5 else float(sys.argv[5])
     
    if sys.argv[4] == "jd":
        hits_list = top_pairs_by_function(int(sys.argv[3]), sys.argv[1], util.get_jaccard_dist, max_bound)
          
    elif sys.argv[4] == "ld":
        hits_list = top_pairs_by_function(int(sys.argv[3]), sys.argv[1], util.get_length_difference, max_bound)
          
    else:
        raise ValueError("Error: Invalid argument for sorting metric (must input 'jd' or 'ld')")
        return
         
    print "finished finding top pairs"
    print "hits_list: ", hits_list
    print_hit_input_list_to_csv(align_list_of_hits(hits_list), sys.argv[2])


if __name__ == "__main__":
    main()
    
    
    
    

    
    

