import sys
import csv
import json
from functions import precision, recall, f1

"""
Processes the results for workers based gold-standard Edinburgh++ HITs
Generates the following outputs:
    - A CSV list of all users who completed an Edinburgh HIT, with stats on 
      their performance (on Edinburgh and on the training HITs)
    - A CSV file with the average statistics for all input batches
    - A CSV listing all HIT ids, as well as average performances on each HIT 
      (used mostly as a sanity check)
arg 1: a CSV file containing two columns. For each row, 
    - The 1st column, entitled "batch_type" states the name of the batch type
    - The 2nd column, entitled "filename" states the filename of the 
      corresponding batch file 
arg 2: CSV of worker scores for training (output of 
       generate_worker_scores_training.py)
arg 3: output CSV file for worker stats
arg 4: output CSV file for average stats for each batch

The qa_worker_dict dictionary maps workerID to a list of statistics regarding the 
worker:
qa_worker_list[0] = # of completed HITs
qa_worker_list[1] = type of qualification user had
qa_worker_list[2] = average precision
qa_worker_list[3] = average recall
qa_worker_list[4] = average F1
qa_worker_list[5] = did worker complete training (yes or no)

The training_worker_dict dictionary maps workerID to a list of statistics regarding
the worker's training performance:
train_worker_dict[0] = precision (initial)
train_worker_dict[1] = recall (initial)
train_worker_dict[2] = f1 (initial)
train_worker_dict[3] = precision (final)
train_worker_dict[4] = recall (final)
train_worker_dict[5] = f1 (final)

The qual_type_dict dictionary maps each qualification type to a list of
statistics regarding the average performance of workers with that qual type:
stats[0] = # of workers
stats[1] = # of HITs
stats[2] = average precision (by HITs)
stats[3] = average recall (by HITs)
stats[4] = average f1 (by HITs)
stats[5] = average precision (by worker)
stats[6] = average recall (by worker)
stats[7] = average f1 (by worker)
"""


""" Scans through all entries in the batch results and constructs a dictionary 
    of workers and their stats """
def scan_results(qual_type, filename, qa_worker_dict, train_worker_dict):
    print("****************************************************")
    print(qual_type)
    print(filename)
    print("****************************************************")
    
    # open input files
    results = csv.reader(open(filename, 'rU'), delimiter = ",")
    print("CSV opened")
    
    # get row numbers for important values from the CSV file
    f_row = next(results)   
    print("starting scan for row titles")
    for i in range(0, len(f_row)):
        if f_row[i] == "HITId":
            hit_id_i = i
        if f_row[i] == "WorkerId":
            worker_id_i = i
        if f_row[i] == "Input.hitType" or f_row[i] == "Input.type":
            type_i = i
        if f_row[i] == "Answer.sureAlignments":
            sub_sure_align_i = i
        if f_row[i] == "Answer.possAlignments":
            sub_poss_align_i = i
        if f_row[i] == "Input.sureAlignments":
            in_sure_align_i = i
        if f_row[i] == "Input.possAlignments":
            in_poss_align_i = i
        if f_row[i][:26] == "Input.answerSureAlignments":
            ans_sure_align_i = i
        if f_row[i][:26] == "Input.answerPossAlignments":
            ans_poss_align_i = i
            
    print("hit_id_i: " + str(hit_id_i))
    print("sub_sure_align_i: " + str(sub_sure_align_i))
    print("in_sure_align_i: " + str(in_sure_align_i))
    print("ans_sure_align_i: " + str(ans_sure_align_i))

    print("starting to scan rows")
    for row in results:
        try:
            hit_id = row[hit_id_i]
            worker_id = row[worker_id_i]

            print("")
            print(hit_id)
            print(worker_id)
            
            # skip all non-test lines
            if (not row[type_i] == "test" or 
                (worker_id == "AURYD2FH3FUOQ" and qual_type == "all")):
                continue
            
            print("")
            print(row)
            print("HITID: " + str(hit_id))
            print("WORKERID: " + str(worker_id))
            print("QUAL TYPE: " + qual_type)
            
            # make corrections to fields labeled "unchanged" or "{}"
            if row[sub_sure_align_i] == "unchanged":
                row[sub_sure_align_i] = row[in_sure_align_i]
            if row[sub_poss_align_i] == "unchanged":
                row[sub_poss_align_i] = row[in_poss_align_i]
            for i in [ans_sure_align_i, ans_poss_align_i, sub_sure_align_i, 
                      sub_poss_align_i]:
                if row[i] == "{}":
                    row[i] = ""
            
            sure_submission = row[sub_sure_align_i]
            poss_submission = row[sub_poss_align_i]
            sure_answer = row[ans_sure_align_i]
            poss_answer = row[ans_poss_align_i]
            print("defined rows")
                
            # convert all alignments to sets
            sure_submission_set = set(sure_submission.split())
            print("SURE_SUBMISSION_STRING: " + str(sure_submission))
            print("SURE_SUBMISSION_SET: " + str(sure_submission_set))
            all_submission_set = (set(poss_submission.split()) | 
                                  sure_submission_set)
            print("ALL_SUBMISSION_SET: " + str(all_submission_set))
            sure_answer_set = set(sure_answer.split())
            print("SURE_CONTROL_SET: " + str(sure_answer_set))
            all_answer_set = set(poss_answer.split()) | sure_answer_set
            print("ALL_CONTROL_SET: " + str(all_answer_set))
            
            # create a list of accuracy stats for the current HIT
            # stats_list[0] = precision, stats_list[1] = recall, stats_list[2] = f1
            stats_list = [precision(sure_submission_set, all_answer_set), 
                          recall(all_submission_set, sure_answer_set)]
            print("STATS_LIST_INITIAL: " + str(stats_list))
            stats_list.append(f1(stats_list[0], stats_list[1]))
            print("STATS_LIST_FINAL: " + str(stats_list))
            
            # add worker to qa_worker_dict
            # the case where worker does not exist in qa_worker_dict
            if worker_id not in qa_worker_dict:
                qa_worker_list = [1, qual_type]
                qa_worker_list = qa_worker_list + stats_list
                qa_worker_dict[worker_id] = qa_worker_list
            
            # the case where worker already exists in qa_worker_dict
            else: 
                qa_worker_list = qa_worker_dict[worker_id]
                qa_worker_list[0] = qa_worker_list[0] + 1
                for i in range(0, 3):
                    qa_worker_list[i + 2] = (float(qa_worker_list[i + 2]) + 
                                          ((stats_list[i] - qa_worker_list[i + 2]) 
                                           / float(qa_worker_list[0])))
            
        except:
            pass

""" Generates a dictionary of workers based on their training performance """
def generate_worker_stats_dict():
    # open input and output files
    training_results = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
    
    train_worker_dict = {}
    
    # enter all workers encountered into train_worker_dict
    for row in training_results:
        try:
            worker_id = row[0]
            train_worker_list = row[4:7] + row[10:13]
            train_worker_dict[worker_id] = train_worker_list
        
        except:
            pass
    
    return train_worker_dict

""" Prints a list of all workers, along with their average accuracy performance"""
def print_worker_stats(qa_worker_dict, train_worker_dict):
    # open output file
    workers_writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = ",")
    workers_writer.writerow(["Worker ID", "# completed HITs ", 
                                  "Qualification Type", "Precision", "Recall", 
                                  "F1", "Training Precision (initial)", 
                                  "Training Recall (initial)", 
                                  "Training F1 (initial)", 
                                  "Training Precision (final)", 
                                  "Training Recall (final)", 
                                  "Training F1 (final)"])
        
    # output all workers in qa_worker_dict
    for worker_id in qa_worker_dict:
        print("WORKER_ID: " + str(worker_id))
        print_list = [worker_id] + qa_worker_dict[worker_id]
        
        if worker_id in train_worker_dict:
            print_list = print_list + train_worker_dict[worker_id]
        
        print("PRINT_LIST: " + str(print_list))
        workers_writer.writerow(print_list)

""" Scans through all workers in worker_dict and finds average stats according 
to worker's qualification type 
"""
def print_average_stats(qa_worker_dict):
    # open output file
    ave_stats_writer = csv.writer(open(sys.argv[4], 'wb'), delimiter = ",")
    ave_stats_writer.writerow(["qual_type", "num_workers", "num_HITs_completed", 
                               "precision (by HITs)", "recall (by HITs)", 
                               "f1 (by HITs)", "precision (by worker)", 
                               "recall (by worker)", "f1 (by worker)"])
    
    qual_type_dict = {} 
    
    # scan through all workers and collect stats based on qual type
    for worker in qa_worker_dict:
        try:
            worker_list = qa_worker_dict[worker] 
            qual_type = worker_list[1]
            num_hits = worker_list[0] 
            
            print("\nWORKER: " + worker + "\nQUAL TYPE: " + qual_type)
            
            # in the case that this is our first time encountering this qual type
            if qual_type not in qual_type_dict:
                print("first time encountering qual type")
                stats = [1, num_hits, worker_list[2] * num_hits, worker_list[3] 
                         * num_hits, worker_list[4] * num_hits, worker_list[2], 
                         worker_list[3], worker_list[4]]
                qual_type_dict[qual_type] = stats
                print(stats)
            
            # the case where we've already seen workers of this qual type 
            else:
                print("already seen this qual type")
                stats = qual_type_dict[qual_type]
                stats[0] = stats[0] + 1
                stats[1] = stats[1] + num_hits
                for i in range(2, 5):
                    stats[i] = stats[i] + worker_list[i] * num_hits
                for i in range(5, 8):
                    stats[i] = float(stats[i]) + ((worker_list[i - 3] - 
                                                   stats[i]) / float(stats[0]))
                print(stats)   
        except:
            pass
                 
    # print out results to writer
    for qual_type in qual_type_dict:
        stats = qual_type_dict[qual_type]
        for i in range(2, 5):
            stats[i] = stats[i] / float(stats[1])
        ave_stats_writer.writerow([qual_type] + qual_type_dict[qual_type])


def main():
    # open all input and output files
    list_batches = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")

    
    # create JSON for dictionary mapping workerID -> training scores
    train_worker_dict = generate_worker_stats_dict()
    
    print("TRAIN_WORKER_DICT: " + str(train_worker_dict))
    
    # scan and analyze all HITs in the batches
    qa_worker_dict = {}
    for row in list_batches:
        try:
            if row[0] == "batch_type":
                continue
            
            scan_results(row[0], row[1], qa_worker_dict, train_worker_dict)
        except:
            pass
    
    print("QA_WORKER_DICT: " + str(qa_worker_dict))
    
    # print CSV of worker performance
    print("printing worker stats")
    print_worker_stats(qa_worker_dict, train_worker_dict)
    
    # print CSV of average performances 
    print("printing average stats")
    print_average_stats(qa_worker_dict)
    
    # dump qa_worker_dict as a JSON file
    json_filename = sys.argv[3][:-3] + "json"
    with open(json_filename, 'wb') as json_writer:
        json.dump(qa_worker_dict, json_writer)
    
if __name__ == "__main__":
    main()
    