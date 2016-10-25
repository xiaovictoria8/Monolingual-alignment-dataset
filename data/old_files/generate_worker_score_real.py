import sys
import csv
from functions import precision, recall, f1

"""
Processes the results for workers on the gold-standard Edinburgh++ HITs.
Generates the following outputs:
    - A CSV list of all users who completed an Edinburgh HIT, with stats on their performance (on Edinburgh and on the training HITs)
    - A CSV file with the average statistics for each of the three batches
arg 1: batch results for "passed alignment training" workers
arg 2: batch results for "participated in alignment training" workers
arg 3: batch results for "all" workers
arg 4: CSV of worker scores for training (output of generate_worker_scores_training.py)
arg 5: CSV of initial Edinburgh HITs input file 
arg 6: output file for worker stats
arg 7: output file for average stats for each batch

The JSON/worker_dict dictionary maps workerID to a list of statistics regarding the worker. For each list,
worker_list[0] = # of completed HITs
worker_list[1] = type of qualification user had
worker_list[2] = average precision
worker_list[3] = average recall
worker_list[4] = average F1
"""
# scans through the results CSV file and updates worker_dict with stats on the worker
def scan_results(qual_type, results, worker_dict):
    for row in results:
        try:
            workerId = row[15]
            
            # skip first line
            if row[0] == "HITId":
                continue
            print(row[0])
            print("WORKERID: " + workerId)
            
            # if an "unchanged" value is encountered, replace with the proper value
            if row[50] == "unchanged": #sureAlignments
                row[50] = row[31]
            
            # convert all alignment results to sets
            sure_sub = set(row[50].split())
            sure_ans = set(row[35].split())
             
            # calculate stats of worker and store in stats_list
            # stats_list[0] = precision, stats_list[1] = recall, stats_list[2] = f1
            stats_list = [precision(sure_sub, sure_ans), recall(sure_sub, sure_ans)]
            stats_list.append(f1(stats_list[0], stats_list[1]))

            # if answer key has two possible alignments, take one with the higher f1
            if row[39]:
                sure_ans_2 = set(row[39].split())
                stats_list_2 = [precision(sure_sub, sure_ans_2), recall(sure_sub, sure_ans_2)]
                stats_list_2.append(f1(stats_list_2[0], stats_list_2[1]))
                print("1st F1 value: " + str(stats_list[2]))
                print("2nd F1 value: " + str(stats_list_2[2]))
            
                if stats_list_2[2] > stats_list[2]:
                    print("selected answer 2")
                    stats_list = stats_list_2
                else:
                    print("selected answer 1")
                
            # add worker to worker_dict
            # the case where worker does not exist in worker_dict
            if workerId not in worker_dict:
                worker_list = [1, qual_type]
                worker_list = worker_list + stats_list
                worker_dict[workerId] = worker_list
            
            # the case where worker already exists in worker_dict
            else:
                worker_list = worker_dict[workerId]
                worker_list[0] = worker_list[0] + 1
                worker_list[2] = float(worker_list[2]) + ((stats_list[0] - worker_list[2]) / float(worker_list[0]))
                worker_list[3] = float(worker_list[3]) + ((stats_list[1] - worker_list[3]) / float(worker_list[0]))
                worker_list[4] = float(worker_list[4]) + ((stats_list[2] - worker_list[4]) / float(worker_list[0]))
            
        except:
            pass
        
        print("")

    return

# scans through all workers in worker_dict and finds average stats according to worker's qualification type
def find_average_stats(worker_dict, ave_stats_writer):
    # stats[0] = # of workers, stats[1] = qualification type, stats[2] = average precision, stats[3] = average recall, stats[4] = average f1
    stats_type_dict = {"passed" : [0, -1, -1, -1], 
                       "participated" : [0, -1, -1, -1],
                       "all" : [0, -1, -1, -1]}
    for worker in worker_dict:
#         print(worker)
        try:
            worker_list = worker_dict[worker] # list of worker stats
            stats = stats_type_dict[worker_list[1]] # list of stats for qual type
#             print(worker_list[1])
#             print("BEFORE STATS: " + str(stats))
#             print("CURRENT STATS: " + str(worker_list))
            
            # the case where this is the first worker we've found of this qual type
            if stats[0] == 0:
                print("no previously existing stats")
                stats[0] = stats[0] + 1
                stats[1] = worker_list[2]
                stats[2] = worker_list[3]
                stats[3] = worker_list[4]
                
            # the case where we've already seen workers of this qual type 
            else:
                print("yes previously existing stats")
                stats[0] = stats[0] + 1
                stats[1] = float(stats[1]) + ((worker_list[2] - stats[1]) / float(stats[0]))
                stats[2] = float(stats[2]) + ((worker_list[3] - stats[2]) / float(stats[0]))
                stats[3] = float(stats[3]) + ((worker_list[4] - stats[3]) / float(stats[0]))
#             
#             print("AFTER STATS: " + str(stats))
#             
#             print("")
#            
        except:
            pass
                 
    # print out results to writer
    for stats_type in stats_type_dict:
        write_list = [stats_type] + stats_type_dict[stats_type]
        ave_stats_writer.writerow(write_list)
        
    return

# print a list of all workers, along with their average accuracy performance
def print_worker_stats(worker_dict):
    # open input and output files
    training_results = csv.reader(open(sys.argv[4], 'rU'), delimiter = ",")
    print_worker_writer = csv.writer(open(sys.argv[6], 'wb'), delimiter = ",")
    print_worker_writer.writerow(["workerid", "num_completed_HITs", "qualification_type", "precision", "recall", "f1", "precision_training_inital", "recall_training_initial", "f1_training_initial", "precision_training_final", "recall_training_final", "f1_training_final"])
    
    # output users who participated in training
    for row in training_results:
        workerId = row[0]
        
        if row[0] not in worker_dict:
            continue
        
        if worker_dict[workerId][1] == "passed" or worker_dict[workerId][1] == "participated":
            print_list = [workerId] + worker_dict[workerId] + row[4:7] + row[10:13]
            print_worker_writer.writerow(print_list)
        
    # output users who did not particiapte in training
    for workerId in worker_dict:
        worker_list = worker_dict[workerId]
        if worker_list[1] == "all":
            print_worker_writer.writerow([workerId] + worker_dict[workerId])
        
    return

def find_automatic_alignment_stats(ave_stats_writer):
    # open input files
    hits_input = csv.reader(open(sys.argv[5], 'rU'), delimiter = ",")
    
    hits_num = 0
    ave_stats = []
    for row in hits_input:
        try:
            # skip first line
            if row[0] == "source":
                continue
            
            print(row[0])
            print(hits_num + 1)
            
            # convert all alignment results to sets
            sure_sub = set(row[4].split())
            sure_ans = set(row[8].split())
            
            # calculate stats of alignment results
            stats_list = [precision(sure_sub, sure_ans), recall(sure_sub, sure_ans)]
            stats_list.append(f1(stats_list[0], stats_list[1]))
            
            # if answer key has two possible alignments, take one with the higher f1
            if row[12]:
                print("two answers exists")
                sure_ans_2 = set(row[12].split())
                stats_list_2 = [precision(sure_sub, sure_ans_2), recall(sure_sub, sure_ans_2)]
                stats_list_2.append(f1(stats_list_2[0], stats_list_2[1]))
                print("1st F1 value: " + str(stats_list[2]))
                print("2nd F1 value: " + str(stats_list_2[2]))
            
                if stats_list_2[2] > stats_list[2]:
                    print("selected answer B")
                    stats_list = stats_list_2
                else:
                    print("selected answer A")
                
            # add values to the average calculation
            # the case where this is the first HIT in the list
            if hits_num == 0:
                hits_num += 1
                ave_stats = stats_list
            
            # the case where this is not the first HIT in the list
            else:
                hits_num += 1
                for i in range(0, 3):
                    ave_stats[i] = float(ave_stats[i]) + ((stats_list[i] - ave_stats[i]) / float(hits_num))
            
            print(ave_stats)
            print("")
            
        except:
            pass
    
    # print averages
    ave_stats_writer.writerow(["automatic_alignments", hits_num] + ave_stats)
    
    return
    

def main():
    # open all input and output files
    passed_training = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    participated_training = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
    all_workers = csv.reader(open(sys.argv[3], 'rU'), delimiter = ",")
    ave_stats_writer = csv.writer(open(sys.argv[7], 'wb'), delimiter = ",")
    ave_stats_writer.writerow(["qual_type", "num_HITs_completed", "precision", "recall", "f1"])
    
    # scan through each HIT result in the batches
    worker_dict = {}
    scan_results("passed", passed_training, worker_dict)
    scan_results("participated", participated_training, worker_dict)
    scan_results("all", all_workers, worker_dict)
    
    # output list of all workers and their stats
    print_worker_stats(worker_dict)
    
    # output the average stats of all workers in each qualification
    find_average_stats(worker_dict, ave_stats_writer)
    
    # output the average stats of the automatically generated alignments
    find_automatic_alignment_stats(ave_stats_writer)
    
    
    
if __name__ == "__main__":
    main()