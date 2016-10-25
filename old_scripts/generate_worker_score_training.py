import json
import csv
import sys
from functions import precision, recall, f1

"""
Creates a CSV file of all workers who completed at least one HIT in the training set.
Each row in the CSV will contain the worker's MT ID and stats about their HIT completion/approval rates and accuracy
arg 1: alignment training HIT results (ie. Batch_[some number]_batch_results.csv)
arg 2: JSON file of previous workers scanned
arg 3: output .csv file
arg 4: output list of all qualified users (users with >16 completed HITs and 80% accuracy)
arg 5: output list of non-qualified users
arg 6: output list of HITs and completion stats 

The JSON/worker_dict dictionary maps workerID to a list of statistics regarding the worker. For each list,
worker_list[0] = # of completed HITs
worker_list[1] = # of correct HITs (100% accuracy)
worker_list[2] = correctness rate (accepted HITs / completed HITs)
worker_list[3] = Precision of answers upon initial submission
worker_list[4] = Recall of answers upon initial submission
worker_list[5] = F1 rating of answers upon initial submission
worker_list[6] = Precision of answers upon seeing answer key
worker_list[7] = Recall of answers upon seeing answer key
worker_list[8] = F1 rating of answers upon seeing answer key
worker_list[9] = a list of all HITs that have been completed by the worker
"""

# scans through each HIT (ie. row) in the input .csv and updates worker stats 
def scan_csv(results, worker_dict, hits_result_writer):
    # Dictionary indexes hits by hitId, each hitId maps to a list 
    # where l[0] = # hits completed and l[1] = # hits correct
    hits_dict = {}
    
    num_rows = 0
    for row in results:
        print(num_rows)
        num_rows += 1
        try:
            hitId = row[0]
            workerId = row[15]
            
            print("hitId: "  + hitId)
            print("workerId: "  + workerId)
            
            # skip first line
            if hitId == "HITId":
                continue    
            
            ### skip HITs 311HQEI8RS1Q91M7H2OGRN5V4US7ZI and 37Y5RYYI0PQNN46K4NY6PTLGJI8SXE
            ### This is because those HITs have strange answer values
            if hitId == "311HQEI8RS1Q91M7H2OGRN5V4US7ZI" or hitId == "37Y5RYYI0PQNN46K4NY6PTLGJI8SXE":
                continue
            
            # if an "unchanged" value is encountered, replace with the proper value
            if row[48] == "unchanged": #sureAlignments
                row[48] = row[31]
            if row[42] == "unchanged": #possAlignments
                row[42] = "{}"
            if row[44] == "unchanged": #sourceHighlights
                row[44] = "{}"
            if row[50] == "unchanged": #targetHighlights
                row[50] = "{}"
            
            # convert all alignment results to sets
            sure_sub_f = set(row[48].split())
            sure_sub_i = set(row[49].split())
            sure_ans = set(row[35].split())
            pos_sub_f = set(row[42].split())
            pos_sub_i = set(row[43].split())
            pos_ans = set(row[36].split())
            src_sub_f = set(row[44].split())
            src_sub_i = set(row[45].split())
            src_ans = set(row[37].split())
            tgt_sub_f = set(row[50].split())
            tgt_sub_i = set(row[51].split())
            tgt_ans = set(row[38].split())
            
            prec_i = precision(sure_sub_i, sure_ans)
            print("prec_i" + str(prec_i))
            rec_i = recall(sure_sub_i, sure_ans)
            print("rec_i" + str(rec_i))
            f1_i = f1(prec_i, rec_i)
            print("f1_i" + str(f1_i))
            prec_f = precision(sure_sub_f, sure_ans)
            print("prec_f" + str(prec_f))
            rec_f = recall(sure_sub_f, sure_ans)
            print("rec_f" + str(rec_f))
            f1_f = f1(prec_f, rec_f)
            print("f1_f" + str(f1_f))
                        
            # create dictionary of HITs data
            if hitId not in hits_dict:
                hits_list = [1, 0]
                hits_dict[hitId] = hits_list
            else:
                hits_list = hits_dict[hitId]
                hits_list[0] = hits_list[0] + 1
            
            # the case where the worker does not exist in worker_dict
            if workerId not in worker_dict:
                # initialize initial worker_list
                completed_HITs = [hitId]
                worker_list = [1, 0, 0, prec_i, rec_i, f1_i, prec_f, rec_f, f1_f, completed_HITs]
                worker_dict[workerId] = worker_list
                
                # check if user's final submission is correct
                if sure_sub_f == sure_ans and pos_sub_f == pos_ans and src_sub_f == src_ans and tgt_sub_f == tgt_ans:
                    print("Correct submission")
                    worker_list[1] = worker_list[1] + 1
                    hits_list[1] = hits_list[1] + 1 ### DELETE THIS LATER, DEBUGGING ONLY
                    
                # print out errors if encountered
                if sure_sub_f != sure_ans:
                    print("Sure alignments incorrect, expected " + str(sure_ans) + ", got " + str(sure_sub_f))
                
                if pos_sub_f != pos_ans:
                    print("Possible alignments incorrect, expected " + str(pos_ans) + ", got " + str(pos_sub_f))
                    
                if src_sub_f != src_ans:
                    print("Source highlights incorrect, expected " + str(src_ans) + ", got " + str(src_sub_f))
                    
                if tgt_sub_f != tgt_ans:
                    print("Target highlights incorrect, expected " + str(tgt_ans) + ", got " + str(tgt_sub_f))
                
                #change correctness rate
                worker_list[2] = worker_list[1]
                    
            # the case where the worker already exists in work_dict
            else:
                
                worker_list = worker_dict[workerId]
                
                # if user has already completed this HIT, skip
                if hitId in worker_list[9]:
                    continue
            
                # mark the worker as having completed this HIT
                worker_list[9].append(hitId)
                
                
                # increase worker's completed HIT count   
                worker_list[0] = worker_list[0] + 1
                
                # check if user's final submission is correct
                if sure_sub_f == sure_ans and pos_sub_f == pos_ans and src_sub_f == src_ans and tgt_sub_f == tgt_ans:
                    print("Correct submission")
                    worker_list[1] = worker_list[1] + 1
                    hits_list[1] = hits_list[1] + 1 
                    
                ### print out errors if encountered
                if sure_sub_f != sure_ans:
                    print("Sure alignments incorrect, expected " + str(sure_ans) + ", got " + str(sure_sub_f))
                
                if pos_sub_f != pos_ans:
                    print("Possible alignments incorrect, expected " + str(pos_ans) + ", got " + str(pos_sub_f))
                    
                if src_sub_f != src_ans:
                    print("Source highlights incorrect, expected " + str(src_ans) + ", got " + str(src_sub_f))
                    
                if tgt_sub_f != tgt_ans:
                    print("Target highlights incorrect, expected " + str(tgt_ans) + ", got " + str(tgt_sub_f))

                    
                # update correctness rate
                worker_list[2] = float(worker_list[1]) / float(worker_list[0])
                
                # update precision, recall and f1 for initial guesses
                worker_list[3] = float(worker_list[3]) + ((prec_i - worker_list[3]) / float(worker_list[0]))
                
                worker_list[4] = float(worker_list[4]) + ((rec_i - worker_list[4]) / float(worker_list[0]))
                
                worker_list[5] = float(worker_list[5]) + ((f1_i - worker_list[5]) / float(worker_list[0]))
                
                # update precision, recall and f1 after seeing answer key
                worker_list[6] = float(worker_list[6]) + ((prec_f - worker_list[6]) / float(worker_list[0]))
                
                worker_list[7] = float(worker_list[7]) + ((rec_f - worker_list[7]) / float(worker_list[0]))
                
                worker_list[8] = float(worker_list[8]) + ((f1_f - worker_list[8]) / float(worker_list[0]))
            
            print("")
            
        except:
            pass
        
    # write HITs statistics 
    for hitId in hits_dict:
        hits_list = hits_dict[hitId]
        hits_result_writer.writerow([hitId, hits_list[0], hits_list[1], float(hits_list[1]) / float(hits_list[0])])
        print (str(hitId) + ":  [" + str(hits_list[0]) + ", " + str(hits_list[1]) + ", " + str((float(hits_list[1]) / float(hits_list[0]))) + "]")
    print("")
        
    return

#goes through all workers in worker_dict and outputs them as a row in the output_writer
def process_workers(worker_dict, output_writer, qual_workers_writer, non_qual_workers_writer):
    
    # defining values for baseline (ie. the performance of the automated aligner)
    prec_ave = 0.810504846031162
    rec_ave = 0.705193071611835
    f1_ave = 0.724704704840528
    baseline_stats = [prec_ave, rec_ave, f1_ave]
    
    for workerId in worker_dict:
        stat_list = worker_dict[workerId]
        diff_stats = []
        for i in range(0, 3):
            diff_stats.append(stat_list[3+i] - baseline_stats[i])
        
        output_writer.writerow([workerId, stat_list[0], stat_list[1], stat_list[2], stat_list[3], stat_list[4], stat_list[5], diff_stats[0], diff_stats[1], diff_stats[2], stat_list[6], stat_list[7], stat_list[8]])
    
        #output workers to qual_workers_writer if that have >16 completed HITs and >80% accuracy
        if stat_list[0] >= 16 and stat_list[2] > 0.8:
            qual_workers_writer.writerow([workerId, 1])
        else:
            non_qual_workers_writer.writerow([workerId, 1])            
        
    print("")
    
    return

def main():
    # open input and qualified workers .csv files
    results = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    output_writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = "\t")
    qual_workers_writer = csv.writer(open(sys.argv[4], 'wb'), delimiter = "\t")
    non_qual_workers_writer = csv.writer(open(sys.argv[5], 'wb'), delimiter = "\t")
    hits_result_writer = csv.writer(open(sys.argv[6], 'wb'), delimiter = "\t")

    # read in JSON data from worker_dict
    with open(sys.argv[2], 'rb') as wd_reader:
        wd_string = wd_reader.read()
    
    # change this back to json.loads(wd_string) in the final version
    worker_dict = json.loads(wd_string)
    
    # scan through each HIT result in the batch
    hits_result_writer.writerow(["hitId", "# submissions", "# correct submissions", "correctness rate"])
    scan_csv(results, worker_dict, hits_result_writer)
    
    # print list of workers in output_writer
    output_writer.writerow(["workerID", "completed_HITs", "correct_HITs", "HIT_correctness_rate", "initial_precision", "initial_recall", "initial_f1", "initial_precision_difference_from_baseline", "initial_recall_difference_from_baseline", "initial_f1_difference_from_baseline", "final_precision", "final_recall", "final_f1"])
    qual_workers_writer.writerow(["workerid", "score"])
    non_qual_workers_writer.writerow(["workerid", "score"])
    process_workers(worker_dict, output_writer, qual_workers_writer, non_qual_workers_writer)
    
    # dump JSON file
    with open(sys.argv[2], 'wb') as wd_writer:
        json.dump(worker_dict, wd_writer)
    
    
if __name__ == "__main__":
    main()