import sys
import csv
import random

def random_csv_embed(f1, f2, outfile):
    """
    Creates a new outfile CSV, which consists of a randomly generated merge of the items in the
    f1 and f2 CSVs.
    Note that in outfile, the order of items originally from f1 will still remain in sequential order.
    This script also deletes any entries in f1 that also exist in f2
    
    Args:
        f1 : The filename of the first CSV file (unaligned HITs) to randomly combine
        f2 : The filename of the second CSV file (QA HITs) to randomly combine
        outfile : The filename of the output CSV file
        
    """
    
    # read the contents of f1 and f2 into lists
    with open(f1, 'rb') as f1_o:
        f1_rd = csv.reader(f1_o, delimiter = ',', quotechar="\"")
        f1_l = list(f1_rd)
        f1_l.pop(0)
        
    with open(f2, 'rb') as f2_o:
        f2_rd = csv.reader(f2_o, delimiter = ',', quotechar="\"")
        f2_l = list(f2_rd)
        f2_l.pop(0)
        
    all_pair_ids = set([hit[0] for hit in f2_l]) # set of the pair ids that exist in the document so far
        
    # generate a random list of line numbers in f2 that lines in f1 should be embedded after
    order_l = [random.choice(xrange(0, len(f2_l))) for i in xrange(0, len(f1_l))]
    order_l.sort()
    print "order_l: ", order_l
    
    # print lines from both files in merged order
    with open(outfile, 'w') as out_o:
        out_writer = csv.writer(out_o, delimiter = ',', quotechar="\"")
        
        out_writer.writerow(["pairID", "documentID", "segmentID", "hitType", "source",
                     "target", "sourceLemmatized", "targetLemmatized",
                     "jaccardDistance", "lengthDifference", "sureAlignments", 
                     "possAlignments", "sourceHighlights", "targetHighlights", 
                     "answerSureAlignments", "answerPossAlignments",
                     "answerSourceHighlights", "answerTargetHighlights"])
    
        order_l_index = 0 # the line number for the next line in f1 to be printed
        for f2_index in xrange(0, len(f2_l)):
            print "f2_index", f2_index
            print "order_l_index", order_l_index
            while order_l_index < len(order_l) and order_l[order_l_index] <= f2_index:
                if f1_l[order_l_index][0] not in all_pair_ids:
                    out_writer.writerow(f1_l[order_l_index])
                    print "len(f1_l[order_l_index])", len(f1_l[order_l_index])
                    all_pair_ids.add(f1_l[order_l_index][0])
                order_l_index += 1
            
            out_writer.writerow(f2_l[f2_index])    
            print "len(f2_l[f2_index])", len(f2_l[f2_index])

def main():
    """
    Merges and removes duplicate sentence pairs in the two input files
    
    Args:
        sys.argv[1] : filename of the unaligned input CSV file
        sys.argv[2] : filename of the embedded QA CSV file
        sys.argv[3] : output filename
    """
    
    random_csv_embed(sys.argv[1], sys.argv[2], sys.argv[3])
    

if __name__ == "__main__":
    main()
    