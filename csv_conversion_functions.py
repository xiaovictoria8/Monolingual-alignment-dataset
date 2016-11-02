import hits_class_definitions as hit

import csv

def batch_results_to_hit_results(filename):
    """
    Converts a MT batch results CSV file to a BatchResults object.
    
    Args:
        file: The name of the CSV batch results file.
        
    Returns:
        A BatchResults object corresponding to all result items in the CSV batch results file.
    """
    
    results = csv.reader(open(filename, 'rU'), delimiter = ",")
    
    # dictionary mapping each header name to its column #
    f_row = next(results)
    row_i = { f_row[i] : i for i in xrange(len(f_row))}
    
    # return lists
    results_list = []
    test_list = []
    training_list = []
    
    # convert each row in the CSV to a HITResult
    for row in results:
        hit_result = hit.HITResult(
            pair_id = row[row_i["Input.pairID"]],
            doc_id = row[row_i["Input.documentID"]],
            segment_id = row[row_i["Input.segmentID"]],
            source = row[row_i["Input.source"]],
            target = row[row_i["Input.target"]],
            sure_align = set(row[row_i["Input.sureAlignments"]].split()),
            poss_align = set(row[row_i["Input.possAlignments"]].split()),
            source_hl = set(row[row_i["Input.sourceHighlights"]].split()),
            target_hl = set(row[row_i["Input.targetHighlights"]].split()),
            hit_id = row[row_i["HITId"]],
            hit_type_id = row[row_i["HITTypeId"]],
            worker_id = row[row_i["WorkerId"]],
            
            worker_sure_align = set(row[row_i["Answer.sureAlignments"]].split()) \
                                if not row[row_i["Answer.sureAlignments"]] == "unchanged" \
                                else set(row[row_i["Input.sureAlignments"]].split()),
            worker_poss_align = set(row[row_i["Answer.possAlignments"]].split()) \
                                if not row[row_i["Answer.possAlignments"]] == "unchanged" \
                                else set(row[row_i["Input.possAlignments"]].split()),
            worker_source_hl = set(row[row_i["Answer.sourceHighlights"]].split()) \
                                if not row[row_i["Answer.sourceHighlights"]] == "unchanged" \
                                else set(row[row_i["Answer.sourceHighlights"]].split()),
            worker_target_hl = set(row[row_i["Answer.targetHighlights"]].split()) \
                                if not row[row_i["Answer.targetHighlights"]] == "unchanged" \
                                else set(row[row_i["Answer.targetHighlights"]].split()),
            )
        
        # append hit_result to the correct list
        if row[row_i["Input.hitType"]] == "real":
            results_list.append(hit_result)
        elif row[row_i["Input.hitType"]] == "test":
            hit_result = hit.HITTestResult(
                hit_result = hit_result,
                ans_sure_align = set(row[row_i["Input.answerSureAlignments"]].split()),
                ans_poss_align = set(row[row_i["Input.answerPossAlignments"]].split()),
                ans_source_hl = set(row[row_i["Input.answerSourceHighlights"]].split()),
                ans_target_hl = set(row[row_i["Input.answerTargetHighlights"]].split())
                )
            test_list.append(hit_result)
            
    return hit.BatchResults(
        hit_results = results_list,
        test_results = test_list,
        training_results = training_list
        )
        

def main():
    l = batch_results_to_hit_results("batch_results.csv")
    d = l.__dict__
    
    print "hit_results: ", len(l.hit_results)
    print "test_results: ", len(l.test_results)
    print "training_results: ", len(l.training_results)
    
    for k in d:
        print k
        for h in d[k]:
            print h, "\n"
    
if __name__ == "__main__":
    main()
    
    
