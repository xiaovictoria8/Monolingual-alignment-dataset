
import hits_classes as hit
import hits_io as io

import sys

def convert_test_batch_to_input(tr_list):
    """
    Args:
        tr_list : A list of the embedded QA HITTestResult objects to convert.
        
    Returns:
        A list of the HITTestInput objects resulting the embedded QA BatchResults.
    """
    
    htest_list = []
    
    print "tr_list", tr_list
    
    for result in tr_list:
        print "hi"
        print "RESULT: ", result
        
        pair_id = result.pair_id
        doc_id = result.doc_id
        segment_id = result.segment_id
        source = result.source
        target = result.target
        sure_align = result.sure_align
        poss_align = result.poss_align
        source_hl = result.source_hl
        target_hl = result.target_hl
        ans_sure_align = result.worker_sure_align
        ans_poss_align = result.worker_poss_align
        ans_source_hl = result.worker_source_hl
        ans_target_hl = result.worker_source_hl
    
        htest_list.append(hit.HITTestInput(pair_id, doc_id, segment_id, source, target, sure_align, 
                                           poss_align, source_hl, target_hl, ans_sure_align, 
                                           ans_poss_align, ans_source_hl, ans_target_hl))

    
    return htest_list

def main():
    """
    Opens input data batch results file containing embedded QA HITs and outputs a csv of the QA HITs
    in the MT HITs input format
    
    Args:
        sys.argv[1] : the filename of the embedded QA batch results file
        sys.argv[2] : the filename of the embedded QA HITs MT input file
    """

    
    br = io.csv_to_batch_results(sys.argv[1])
    
    htest_list = convert_test_batch_to_input(br.test_results)
    print "htest_list", htest_list
    
    io.hit_input_list_to_csv(htest_list, sys.argv[2])
    
    
    return 
    
if __name__ == "__main__":
    main()