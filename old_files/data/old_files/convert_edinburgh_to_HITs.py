import json
import csv
import sys
import random
from functions import get_jaccard_dist

"""
Takes in a set of alignments from the Edinburgh corpus in JSON format.
Creates a CSV batch input for alignment hits on Mechanical Turk.

arg 1: Edinburgh JSON input file (ie. train.json)
arg 2: Alignment input file (ie. output.align) 
arg 3: output CSV file
"""

# takes in a csv_reader file and outputs a dictionary mapping docid to alignments
def make_alignment_dict(align_input):
    align_dict = {}
    for row in align_input:
        try:
            align_dict[row[0]] = row[1]
            
        except:
            pass
    
    return align_dict

# takes in an embedded list of alignments (see Edinburgh JSON documentation for formatting)
# outputs alignments in Pharoah format
def extract_alignments(align_list):
    align_str = ""
    for alignment in align_list:
        src = alignment[0]
        tgt_list = alignment[1]
        for tgt in tgt_list:
            align_str = align_str + str(src) + "-" + str(tgt) + " "
    
    return align_str 

def main():
    #open input JSON and alignment files, as well as output CSV file
    with open(sys.argv[1], 'rb') as reader:
        reader_string = reader.read()
    json_input = json.loads(reader_string)
    align_input = csv.reader(open(sys.argv[2], 'rb'), delimiter='\t')
    writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = ",")
    
    # for sentence pairs with two alignments, select which pairs should use A's alignments and which should use C's
    double_aligned_pairs = 380
    list_choose_a = random.sample(range(380), double_aligned_pairs / 2)
    seen_double_aligned_pairs = 0
     
    writer.writerow(["source", "target", "docID", "type", "sureAlignments", "possAlignments", "sourceHighlights", "targetHighlights", "answerSureAlignments1", "answerPossAlignments1", "answerSourceHighlights1", "answerTargetHighlights1", "answerSureAlignments2", "answerPossAlignments2", "answerSourceHighlights2", "answerTargetHighlights2"])
    
    # create a dictionary of automated alignments, indexed by docID
    align_dict = make_alignment_dict(align_input)

    # scan through each pair of paraphrases
    for pair in json_input["paraphrases"]:
        try:
            # define values for each column
            source = pair["S"]["string"]
            target = pair["T"]["string"]
            docID = pair["id"]
            stype = "test"
            sure_alignments = align_dict[docID]
            poss_alignments = "{}"
            source_highlights = "{}"
            target_highlights = "{}"
            answer_source_highlights = "{}"
            answer_target_highlights = "{}"
            
            # extract answer alignments
            if "A" in pair["annotations"] and "C" in pair["annotations"]:
                if seen_double_aligned_pairs in list_choose_a:
                    align_ans = pair["annotations"]["A"]
                else:
                    align_ans = pair["annotations"]["C"]
            elif "A" in "A" in pair["annotations"]:
                align_ans = pair["annotations"]["A"]
            else:
                align_ans = pair["annotations"]["C"]
            
            ans_sure_alignments = extract_alignments(align_ans["S"])
            ans_poss_alignments = extract_alignments(align_ans["P"])
            
            
            if "A" in pair["annotations"]:
                align_ans1 = pair["annotations"]["A"]
                answer_sure_alignments1 = extract_alignments(align_ans1["S"])
                answer_poss_alignments1 = extract_alignments(align_ans1["P"])
                
                if "C" in pair["annotations"]:
                    align_ans2 = pair["annotations"]["C"]
                    answer_sure_alignments2 = extract_alignments(align_ans2["S"])
                    answer_poss_alignments2 = extract_alignments(align_ans2["P"])
                
                else:
                    answer_sure_alignments2 = None
                    answer_poss_alignments2 = None
                    
            elif "C" in pair["annotations"]:
                align_ans1 = pair["annotations"]["C"]
                answer_sure_alignments1 = extract_alignments(align_ans1["S"])
                answer_poss_alignments1 = extract_alignments(align_ans1["P"])
                answer_sure_alignments2 = None
                answer_poss_alignments2 = None
            
            # write row to CSV output
            writer.writerow([source, target, docID, stype, sure_alignments, poss_alignments, source_highlights, target_highlights, answer_sure_alignments1, answer_poss_alignments1, answer_source_highlights, answer_target_highlights, answer_sure_alignments2, answer_poss_alignments2, answer_source_highlights, answer_target_highlights])
            
        except:
            pass

if __name__ == "__main__":
    main()