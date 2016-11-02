import json
import csv
import sys
import random
import functions as func
import stanford_corenlp_functions as sc_func
import nltk

"""
Takes in a set of alignments from the Edinburgh corpus in JSON format.
Creates a CSV batch input for alignment hits on Mechanical Turk.

Also creates a CSV batch results file that contains results for all sentence 
pairs with two annotations.

The batch result displays the alignments of the annotator who was not chosen for
the input HIT.

This batch results file should be used as an input to 
generate_worker_score_from_edinburgh.py to calculate the accuracy scores of the 
other annotator.

arg 1: Edinburgh JSON input file (ie. train.json)
arg 2: sample batch results file (to properly format annotator batch results)
arg 3: output filename for the HITs batch input CSV file
arg 4: output filename for the annotator batch results file
"""

# takes in an embedded list of alignments from Edinburgh JSON file
# outputs alignments in Pharoah format
def extract_alignments(align_list):
    if align_list == []:
        return "{}"
    
    align_str = ""
    for alignment in align_list:
        src = alignment[0]
        tgt_list = alignment[1]
        for tgt in tgt_list:
            align_str = align_str + str(src) + "-" + str(tgt) + " "
    
    return align_str 

def main():
    #open input JSON and alignment files
    with open(sys.argv[1], 'rb') as reader:
        reader_string = reader.read()
    json_input = json.loads(reader_string)
    
    # open and set up output files
    csv_writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = ",")
    csv_writer.writerow(["pairID", "documentID", "segmentID", "hitType", "source",
                         "target", "sourceLemmatized", "targetLemmatized",
                         "jaccardDistance", "lengthDifference", "sureAlignments", 
                         "possAlignments", "sourceHighlights", "targetHighlights", 
                         "answerSureAlignments", "answerPossAlignments",
                         "answerSourceHighlights", "answerTargetHighlights"])
    
    batch_results_reader = csv.reader(open(sys.argv[2], 'r'), delimiter = ",")
    f_row = next(batch_results_reader)   
    
    for i in range(0, len(f_row)):
        if f_row[i] == "HITId":
            hit_id_i = i
        if f_row[i] == "WorkerId":
            worker_id_i = i
        if f_row[i] == "Input.pairID":
            pair_id_i = i
        if f_row[i] == "Input.hitType" or f_row[i] == "Input.type":
            type_i = i
        if f_row[i] == "Input.source":
            src_id_i = i
        if f_row[i] == "Input.target":
            tgt_id_i = i
        if f_row[i] == "Input.sourceLemmatized":
            src_lem_id_i = i
        if f_row[i] == "Input.targetLemmatized":
            tgt_lem_id_i = i
        if f_row[i] == "Input.jaccardDistance":
            jd_i = i
        if f_row[i] == "Input.lengthDifference":
            ld_i = i
        if f_row[i] == "Answer.sureAlignments":
            sub_sure_align_i = i
        if f_row[i] == "Answer.possAlignments":
            sub_poss_align_i = i
        if f_row[i][:26] == "Input.answerSureAlignments":
            ans_sure_align_i = i
        if f_row[i][:26] == "Input.answerPossAlignments":
            ans_poss_align_i = i
    
    batch_results_writer = csv.writer(open(sys.argv[4], 'wb'), delimiter = ",")
    batch_results_writer.writerow(f_row)

    # for sentence pairs with two alignments, select which answer annotation
    double_aligned_pairs = 380 # use 380 for the full set
    list_choose_a = random.sample(range(double_aligned_pairs), 
                                  double_aligned_pairs / 2)
    seen_double_aligned_pairs = 0
    list_choose_a.sort()

    num_a = 0
    num_c = 0
    num_rows = 0 # number of rows to print
    # scan through each pair of paraphrases
    for pair in json_input["paraphrases"]:
        try:
            print("")
            print(num_rows)
            
            if num_rows == 100000:
                break
            
            num_rows += 1
            
            # define values for each column
            source = pair["S"]["string"]
            target = pair["T"]["string"]
            src_lemma = func.get_lemmatized_version(source)
            tgt_lemma = func.get_lemmatized_version(target)
            jd = func.get_jaccard_dist(src_lemma, tgt_lemma)
            print("jd: " + str(jd))
            ld = abs(len(nltk.word_tokenize(source)) - 
                     len(nltk.word_tokenize(target)))
            print("ld: " + str(ld))
            docID = pair["id"]
            stype = "test"
            sure_alignments = sc_func.mono_align(src_lemma, tgt_lemma)
            poss_alignments = "{}"
            source_highlights = "{}"
            target_highlights = "{}"
            answer_source_highlights = "{}"
            answer_target_highlights = "{}"
            align_sub = None
            
            print(docID)
            print("seen_double_aligned_pairs: " + str(seen_double_aligned_pairs))
        
            # "randomly" extract answer alignments
            if "A" in pair["annotations"] and "C" in pair["annotations"]:
                print("two alignments exist")
                if seen_double_aligned_pairs in list_choose_a:
                    print("randomly selected A")
                    num_a += 1
                    align_ans = pair["annotations"]["A"]
                    align_sub = pair["annotations"]["C"]
                    print("align_sub: ")
                    print(str(align_sub))
                    
                else:
                    print("randomly selected C")
                    num_c += 1
                    align_ans = pair["annotations"]["C"]
                    align_sub = pair["annotations"]["A"]
                    print("align_sub: ")
                    print(str(align_sub))
                    
                seen_double_aligned_pairs += 1
            elif "A" in "A" in pair["annotations"]:
                print("only A exists, selected A")
                align_ans = pair["annotations"]["A"]
            else:
                print("only C exists, selected C")
                align_ans = pair["annotations"]["C"]
            
            answer_sure_alignments = extract_alignments(align_ans["S"])
            answer_poss_alignments = extract_alignments(align_ans["P"])
            
            print("SURE ANSWER: " + str(answer_sure_alignments))
            print("POSS ANSWER: " + str(answer_poss_alignments))
            
            # write row to CSV output
            csv_writer.writerow([docID, docID, "", "test", source, target,
                                       src_lemma, tgt_lemma, jd, ld, sure_alignments,
                                       poss_alignments, source_highlights,
                                       target_highlights, answer_sure_alignments,
                                       answer_poss_alignments, answer_source_highlights,
                                       answer_target_highlights])
            
            # if two alignments, print the not chosen one to batch_results_writer
            if align_sub:
                print("align_sub exists")

                sub_sure_alignments = extract_alignments(align_sub["S"])
                sub_poss_alignments = extract_alignments(align_sub["P"])
                
                print("submission alignments extracted")
                print("SURE SUBMISS: " + sub_sure_alignments)
                print("POSS SUBMISS: " + sub_poss_alignments)
                
                # print annotator batch results
                batch_row = [None] * len(f_row)
                batch_row[hit_id_i] = "N/A"
                batch_row[pair_id_i] = docID
                batch_row[type_i] = stype
                batch_row[src_id_i] = source
                batch_row[tgt_id_i] = target
                batch_row[src_lem_id_i] = src_lemma
                batch_row[tgt_lem_id_i] = tgt_lemma
                batch_row[jd_i] = jd 
                batch_row[ld_i] = ld
                batch_row[worker_id_i] = "Edinburgh annotator"
                batch_row[sub_sure_align_i] = sub_sure_alignments # sure submission
                batch_row[sub_poss_align_i] = sub_poss_alignments # possible submission
                batch_row[ans_sure_align_i] = answer_sure_alignments # sure answers
                batch_row[ans_poss_align_i] = answer_poss_alignments # target answers

                print("batch_row created: " + str(batch_row))
                
                batch_results_writer.writerow(batch_row)
                
        except:
            pass

    print("num a: " + str(num_a))
    print("num c: " + str(num_c))
if __name__ == "__main__":
    main()