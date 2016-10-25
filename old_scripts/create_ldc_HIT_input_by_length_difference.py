import sys
import csv
import heapq
import random
import nltk
import functions as func
import stanford_corenlp_functions as sc_func
from progress.bar import Bar


"""
Creates a CSV file that will be used as input for alignment.
Outputs the top n sentence pairs from the input, as sorted by length difference
arg 1: data (ie. all.tsv)
arg 2: Edinburgh HITs template (ie. output of convert_edinburgh_to_HITs.py)
arg 3: CSV output file


pairs_list represents each sentence pair as a list of values:
pair[0] = length difference
pair[1] = pair id (generated by this script)
pair[2] = source sentence
pair[3] = target sentence
pair[4] = lemmatized source sentence 
pair[5] = lemmatized target sentence
pair[6] = document id
pair[7] = segment id
pair[8] = document type
pair[9] = jaccard distance
"""

"""
Returns a list of the top n sentence pairs in ldc, as sorted by length difference
Each sentence pair is represented by a list
"""
def generate_top_pairs(n, ldc, bar):
    pairs_heap = []
    
    num_rows = 0
    for row in ldc:
        try:
            print("")
            print("ROW: " + str(num_rows))
            num_rows += 1
            if (row[7] == "1" or row[5] != "sent"):
                print("Not sentence with possible pairs")
                continue
            
            pair_num = -1
            
            # scan through all possible sentence pairs in the row
            for i in range(8, len(row)):
                for j in range(i+1, len(row)):
                    print("")
                    print("SOURCE: " + str(i) + " " + row[i])
                    print("LENGTH: " + str(len(row[i].split())))
                    print("TARGET: " + str(j) + " " + row[j])
                    print("LENGTH: " + str(len(row[j].split())))
                    
                    pair_num += 1
                    
                    src_token = nltk.word_tokenize(row[i])
                    tgt_token = nltk.word_tokenize(row[j])
                    #only select full sentences that have between 5 and 30 words
                    if (len(tgt_token) < 30 and len(tgt_token) > 5 and 
                    len(src_token) < 30 and len(src_token) > 5
                    and not row[i][0].islower() and not row[j][0].islower()
                    and row[i][len(row[i]) - 1] in "!\".?"
                    and row[j][len(row[j]) - 1] in "!\".?"):

                        # create the tuple representation for this pair
                        # pair_id = [doc id]-[seg id]-[src index]-[tgt index]
                        pair_id = row[2] + "-" + row[3] + "-" + str(pair_num)
                        src = ' '.join(src_token)
                        tgt = ' '.join(tgt_token)
                        src_lemma = func.get_lemmatized_version(row[i])
                        tgt_lemma = func.get_lemmatized_version(row[j])
                        
                        jd = func.get_jaccard_dist(src_lemma, tgt_lemma)
                        ld = abs(len(src_token) - len(tgt_token))
                        
                        
                        # ignore if jaccard distance is too high
                        if jd > 0.9:
                            continue
                        
                        pair = [ld, pair_id, src, tgt, src_lemma, tgt_lemma,
                                row[2], row[3], row[5], jd]
                        
                        print("PAIR: " + str(pair))
                        # insert pair into heap, and discard min element
                        if len(pairs_heap) < n:
                            heapq.heappush(pairs_heap, pair)
                            print("inserted pair into heap")
                         
                        else:
                            p = heapq.heappushpop(pairs_heap, pair)
                            print("removed " + str(p) + " from heap")
                    
                    print("HEAPQ LENGTH: " + str(len(pairs_heap)))
                    
                    bar.next()
                    
        except:
            pass
    
    return pairs_heap

# creates a list of all HITs in the Edinburgh QA template
def generate_qa_list(bar):
    qa_hits = csv.reader(open(sys.argv[2], 'rb'), delimiter = ',')
    
    qa_list = []
    for row in qa_hits:
        if row[0] == "pairID":
            continue
        
        qa_list.append(row)
        
    bar.next()

    return qa_list

# outputs all sentence pairs in jd_dict, along with their doc_id
def output_jd_pairs(jd_dict, qa_list, n, bar):
    # open and setup writer file
    csv_writer = csv.writer(open(sys.argv[3], 'w'), delimiter = ',')
    csv_writer.writerow(["pairID", "documentID", "segmentID", "hitType", "source",
                         "target", "sourceLemmatized", "targetLemmatized",
                         "jaccardDistance", "lengthDifference", "sureAlignments", 
                         "possAlignments", "sourceHighlights", "targetHighlights", 
                         "answerSureAlignments", "answerPossAlignments",
                         "answerSourceHighlights", "answerTargetHighlights"])
    
    # list_choose_qa[i] is the position index in ldc_hits that qa_list[i] should
    # be printed after 
    list_choose_qa = [] 
    for i in range(0, len(qa_list)):
        list_choose_qa.append(int(random.random() * (n + 1)))
    list_choose_qa.sort()
    
    print("QA_LIST: " + str(qa_list))
    print("QA_LIST_LEN: " + str(len(qa_list)))
    print("LIST_CHOOSE_QA: " + str(list_choose_qa))
    print("LIST_CHOOSE_QA_LENGTH: " + str(len(list_choose_qa)))
    
    ldc_hits = 0
    qa_index = 0
    
    for pair in jd_dict:
        try:
            print("")
            print("LDC_HITS: " + str(ldc_hits))
            
            # output item in CSV
            pair_id = pair[1]
    
            doc_id = pair[6]
            seg_id = pair[7]
            source = pair[2]
            target = pair[3]
            source_lemma = pair[4]
            target_lemma = pair[5]
            jd = pair[9]
            ld = pair[0]
            
            print("PAIR_ID: " + pair_id)
            print("DOC_ID: " + doc_id)
            print("SEGMENT_ID: " + seg_id)
            print("SOURCE: " + source)
            print("TARGET: " + target)
            print("SRC_LEMMA: " + source_lemma)
            print("TGT_LEMMA: " + target_lemma)
            
            # use Sultan's monolingual aligner to produce initial alignments
            alignments = sc_func.mono_align(pair[4], pair[5])
            
            # replace commas and quotation marks in all string values
            for i in range(2, 6):
                pair[i] = pair[i].replace('"', '&quot;')
                pair[i] = pair[i].replace("'", '&apos;')
        
            
            poss_align = "{}" 
            source_align = "{}" 
            target_align = "{}"
            csv_writer.writerow([pair_id, doc_id, seg_id, "real", source, target, 
                                 source_lemma, target_lemma, jd, ld, alignments, 
                                 poss_align, source_align, target_align, "{}", 
                                 "{}", "{}", "{}"])
            
            if qa_index >= len(qa_list):
                continue
            
            # output edinburgh HITs if randomly selected
            while list_choose_qa[qa_index] == ldc_hits:
                print("Edinburgh HIT has been randomly selected")
                print("QA_INDEX: " + str(qa_index))
                print("ROW: " + str(qa_list[qa_index]))
                csv_writer.writerow(qa_list[qa_index])
                qa_index += 1
            ldc_hits += 1
            
            bar.next()
        
        except:
            pass
            
    # print out remaining QA HITs
    for i in range(qa_index, len(qa_list)):
        print("Edinburgh HIT has been randomly selected")
        print("QA_INDEX: " + str(i))
        print("ROW: " + str(qa_list[qa_index]))
        csv_writer.writerow(qa_list[i])
                   

def main():
    bar = Bar('Processing', max = 100000)
    
    # open data file
    ldc = csv.reader(open(sys.argv[1], 'rb'), delimiter = '\t', quotechar=None)
    
    n = 500 # number of pairs to generate
    
    # create dictionary of top n pairs
    ldc_list = generate_top_pairs(n, ldc, bar)
    
    # create list of Edinburgh HITs
    qa_list = generate_qa_list(bar)

    print("QA_LIST: " + str(qa_list))
    print("JD_DICT")
    
    # output all items in jd_dict according to the csv format
    output_jd_pairs(ldc_list, qa_list, n, bar)

if __name__ == "__main__":
    main()