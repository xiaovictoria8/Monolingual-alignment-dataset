import sys
import csv
import json

"""
Processes the batch results for LDC HITs based on worker's average results.
Generates the following outputs:
    - A CSV containing only "good" HITs (that is, HITs completed by workers with
      averages above the threshold) in the HIT results format.
    - A CSV containing only "bad" HITs (that is, HITs completed by workers with
      averages below the threshold) in the HIT results format.
    - A TSV list of "underperforming" workers scoring below the average. This 
      file can be used as input for the updateQualification operation for the MT
      CLT.
    - A JSON file containing the complete dataset so far, including the new
      "good" HITs

arg 1: a CSV file containing two columns. For each row, 
    - The 1st column, entitled "batch_type" states the name of the batch type
    - The 2nd column, entitled "filename" states the filename of the 
      corresponding batch file 
arg 2: the worker JSON file (ie. output of generate_worker_score_from_qa_HITs.py)
arg 3: previous "good HITs" batch results CSV
arg 4: output "bad HITs" CSV file
arg 5: output TSV file for underperforming workers
arg 6: previous dataset JSON file

The qa_worker_dict dictionary maps workerID to a list of statistics regarding the 
worker:
qa_worker_list[0] = # of completed HITs
qa_worker_list[1] = type of qualification user had
qa_worker_list[2] = average precision
qa_worker_list[3] = average recall
qa_worker_list[4] = average F1
qa_worker_list[5] = did worker complete training (yes or no)
"""

""" Returns a list all of workers who scored >= n on the QA HITs. 
    Outputs TSV of all workers who scored below n in the scorefile format for
    the MT CLT 
"""
def generate_qualified_workers(n):
    # open input JSON file
    with open(sys.argv[2], 'rb') as wd_reader:
        wd_string = wd_reader.read()
    qa_worker_dict = json.loads(wd_string)
    
    # open underperforming workers TSV file
    workers_writer = csv.writer(open(sys.argv[5], 'wb'), delimiter = "\t")
    workers_writer.writerow(["workerid", "score"])
    
    # process each worker in qa_worker_dict
    qual_workers = []
    for worker_id in qa_worker_dict:
        qa_worker_list = qa_worker_dict[worker_id]
        
        # case where worker scored >n on QA HITs
        if qa_worker_list[4] >= n:
            qual_workers.append(worker_id)
        
        # case where worker did not score >n
        else:
            workers_writer.writerow([worker_id, "0"])

    return qual_workers

""" Scans through all HIT results in filename and prints them to appriopriate
    CSV output
"""
def print_results(filename, qual_workers, good_hits_writer, bad_hits_writer):
    # open input and output files
    results = csv.reader(open(filename, 'rU'), delimiter = ",")
    
    # get row numbers for important values from the CSV file
    f_row = next(results)   
    for i in range(0, len(f_row)):
        if f_row[i] == "HITId":
            hit_id_i = i
        if f_row[i] == "WorkerId":
            worker_id_i = i
        if f_row[i] == "Input.pairID":
            pair_id_i = i
        if f_row[i] == "Input.documentID":
            doc_id_i = i
        if f_row[i] == "Input.segmentID":
            seg_id_i = i
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
        if f_row[i] == "Input.sureAlignments":
            sure_align_i = i
        if f_row[i] == "Input.possAlignments":
            poss_align_i = i
        if f_row[i] == "Input.sourceHighlights":
            src_hl_i = i
        if f_row[i] == "Input.targetHighlights":
            tgt_hl_i = i
    
    n = 0
    m = 0
    for row in results:
        try:
            hit_id = row[hit_id_i]
            worker_id = row[worker_id_i]

            # if worker is qualified, print to good_hits_writer
            if worker_id in qual_workers:
                # skip all test lines
                if row[type_i] == "test":
                    continue
            
                good_hits_writer.writerow(row)
                
            # else, print to bad_hits_writer
            else:
                bad_row = []
                for i in [pair_id_i, doc_id_i, seg_id_i, type_i, src_id_i, 
                          tgt_id_i, src_lem_id_i, tgt_lem_id_i, jd_i, ld_i, 
                          sure_align_i, poss_align_i, src_hl_i, tgt_hl_i]:
                    bad_row.append(row[i])
                for i in range(0, 4):
                    bad_row.append("{}")
                bad_hits_writer.writerow(bad_row)
        except:
            pass

def main():
    n = 0.80 # threshold F1 value for workers to be "qualified"
    
    # open input files and output files for batch results
    list_batches = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    good_hits_writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = ",")
    good_hits_writer.writerow(["pairID", "documentID", "segmentID", "hitType", "source",
                         "target", "sourceLemmatized", "targetLemmatized",
                         "jaccardDistance", "lengthDifference", "sureAlignments",
                         "possAlignments", "sourceHighlights", "targetHighlights", 
                         "answerSureAlignments", "answerPossAlignments",
                         "answerSourceHighlights", "answerTargetHighlights"])
    bad_hits_writer = csv.writer(open(sys.argv[4], 'wb'), delimiter = ",")
    bad_hits_writer.writerow(["pairID", "documentID", "segmentID", "hitType", "source",
                         "target", "sourceLemmatized", "targetLemmatized",
                         "jaccardDistance", "lengthDifference", "sureAlignments",
                         "possAlignments", "sourceHighlights", "targetHighlights", 
                         "answerSureAlignments", "answerPossAlignments",
                         "answerSourceHighlights", "answerTargetHighlights"])
    
    # create list of "good" workers and output TSV of underperforming workers
    qual_workers = generate_qualified_workers(n)
    print(qual_workers)
    
    # scan through batch results and print to the appriopriate output file
    for row in list_batches:
        try:
            if row[0] == "batch_type":
                continue
            
            print_results(row[1], qual_workers, good_hits_writer, 
                          bad_hits_writer)
        except:
            pass
    
    return
    
if __name__ == "__main__":
    main()