import sys
import csv
from functions import precision, recall, f1

"""
Processes the results for workers on gold-standard Edinburgh++ HITs
Generates the following outputs:
    - A CSV list of all users who completed an Edinburgh HIT, with stats on their performance (on Edinburgh and on the training HITs)
    - A CSV file with the average statistics for each of the three batches
    - A CSV listing all HIT ids, as well as average performances on each HIT (used mostly as a sanity check)
arg 1: a CSV file containing two columns. For each row, 
    - The 1st column, entitled "batch_type" states the name of the batch type
    - The 2nd column, entitled "filename" states the filename of the corresponding batch file 
    - This file must include, at least, batches for "passed", "participated" and "all" workers, or an exception will be raised
arg 2: CSV of worker scores for training (output of generate_worker_scores_training.py)
arg 3: output CSV file for worker stats
arg 4: output CSV file for average stats for each batch

The worker_dict dictionary maps workerID to a list of statistics regarding the worker. For each list,
worker_list[0] = # of completed HITs
worker_list[1] = type of qualification user had
worker_list[2] = average precision
worker_list[3] = average recall
worker_list[4] = average F1
"""

""" Scans through all entries in the batch results and constructs a dictionary of workers and their stats """
def scan_results(qual_type, filename, worker_dict):
    print("****************************************************")
    print(qual_type)
    print(filename)
    print("****************************************************")
    results = csv.reader(open(filename, 'rU'), delimiter = ",")
    
    for row in results:
        try:
            hit_id = row[0]
            worker_id = row[15]
            
            # skip first line
            if hit_id == "HITId":
                continue
            
            print("")
            print(row)
            print("HITID: " + str(hit_id))
            print("WORKERID: " + str(worker_id))
            
            # make corrections to fields labeled "unchanged" or "{}"
            if row[50] == "unchanged": 
                row[50] = row[31]
            if row[46] == "unchanged":
                row[46] = row[32]
            for i in [35, 36, 46, 50]:
                if row[i] == "{}":
                    row[i] = ""
            
            sure_submission = row[50]
            poss_submission = row[46]
            sure_control = row[35]
            poss_control = row[36]
                
            # convert all alignments to sets
            sure_submission_set = set(sure_submission.split())
            print("SURE_SUBMISSION_STRING: " + str(sure_submission))
            print("SURE_SUBMISSION_SET: " + str(sure_submission_set))
            all_submission_set = set(poss_submission.split()) | sure_submission_set
            print("ALL_SUBMISSION_SET: " + str(all_submission_set))
            sure_control_set = set(sure_control.split())
            print("SURE_CONTROL_SET: " + str(sure_control_set))
            all_control_set = set(poss_control.split()) | sure_control_set
            print("ALL_CONTROL_SET: " + str(all_control_set))
            
            # create a list of accuracy stats for the current HIT
            # stats_list[0] = precision, stats_list[1] = recall, stats_list[2] = f1
            print("starting stats list calculation")
            stats_list = [precision(sure_submission_set, all_control_set), recall(all_submission_set, sure_control_set)]
            print("STATS_LIST_INITIAL: " + str(stats_list))
            stats_list.append(f1(stats_list[0], stats_list[1]))
            print("STATS_LIST_FINAL: " + str(stats_list))
            
            # add worker to worker_dict
            # the case where worker does not exist in worker_dict
            if worker_id not in worker_dict:
                worker_list = [1, qual_type]
                worker_list = worker_list + stats_list
                worker_dict[worker_id] = worker_list
            
            # the case where worker already exists in worker_dict
            else: 
                worker_list = worker_dict[worker_id]
                worker_list[0] = worker_list[0] + 1
                for i in range(0, 3):
                    worker_list[i + 2] = float(worker_list[i + 2]) + ((stats_list[i] - worker_list[i + 2]) / float(worker_list[0]))
            
        except:
            pass

""" Prints a list of all workers, along with their average accuracy performance"""
def print_worker_stats(worker_dict):
    # open input and output files
    training_results = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
    print_worker_writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = ",")
    print_worker_writer.writerow(["Worker ID", "# completed HITs ", "Qualification Type", "Precision", "Recall", "F1", "Training Precision (initial)", "Training Recall (initial)", "Training F1 (initial)", "Training Precision (final)", "Training Recall (final)", "Training F1 (final)"])
    
    # output users who participated in training
    for row in training_results:
        try:
            worker_id = row[0]
            
            if worker_id not in worker_dict:
                continue
            
            if worker_dict[worker_id][1] == "passed" or worker_dict[worker_id][1] == "participated":
                print_list = [worker_id] + worker_dict[worker_id] + row[4:7] + row[10:13]
                print_worker_writer.writerow(print_list)
        except:
            pass
        
    # output users who did not particiapte in training
    for worker_id in worker_dict:
        worker_list = worker_dict[worker_id]
        if worker_list[1] == "all":
            print_worker_writer.writerow([worker_id] + worker_dict[worker_id])
        
    return

""" Scans through all workers in worker_dict and finds average stats according to worker's qualification type """
def print_average_stats(worker_dict, ave_stats_writer):
    # dictionary mapping each qualification type to a stats list, containing statistics on average precision, recall and f1
    # stats[0] = # of workers, stats[1] = qualification type, stats[2] = average precision, stats[3] = average recall, stats[4] = average f1
    
    print("****************************************************")
    print("PRINTING AVERAGE")
    print("****************************************************")
    
    qual_type_dict = {} 
    
    for worker in worker_dict:
        try:
            worker_list = worker_dict[worker] 
            qual_type = worker_list[1] 
            
            # in the case that this is our first time encountering this qualification type
            if qual_type not in qual_type_dict:
                print("first time encountering qual type")
                stats = [1, worker_list[2], worker_list[3], worker_list[4]]
                qual_type_dict[qual_type] = stats
                print(stats)
            
            # the case where we've already seen workers of this qual type 
            else:
                print("already seen this qual type")
                stats = qual_type_dict[stats]
                stats[0] = stats[0] + 1
                for i in range(1, 4):
                    stats[i] = float(stats[i]) + ((worker_list[i + 1] - stats[i]) / float(stats[0]))
                print(stats)      
        except:
            pass
                 
    # print out results to writer
    for qual_type in qual_type_dict:
        ave_stats_writer.writerow([qual_type] + qual_type_dict[qual_type])
        
    return
    

def main():
    # open all input and output files
    list_batches = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    ave_stats_writer = csv.writer(open(sys.argv[4], 'wb'), delimiter = ",")
    
    # scan through all HITs results in the list of batches to produce dictionary of worker stats
    worker_dict = {}
    
    does_passed_exist = False
    does_participated_exist = False
    does_all_exist = False
    
    for row in list_batches:
        try:
            if row[0] == "batch_type":
                continue
            if row[0] == "passed":
                does_passed_exist = True
            if row[0] == "participated":
                does_participated_exist = True
            if row[0] == "all":
                does_all_exist = True
            scan_results(row[0], row[1], worker_dict)
        except:
            pass
        
    if not does_passed_exist or not does_participated_exist or not does_all_exist :
        raise Exception("list of batches needs to include batches for \"passed\", \"participated\" and \"all\" worker results")
    
    # output list of all workers and their stats
    print_worker_stats(worker_dict)
    
    # output the average stats of all workers in each qualification
    ave_stats_writer.writerow(["qual_type", "num_HITs_completed", "precision", "recall", "f1"])
    print_average_stats(worker_dict, ave_stats_writer)
    
if __name__ == "__main__":
    main()