#!/user/bin/python
import json
import csv
import sets
import sys

"""
Creates a CSV file of all workers to be assigned the "Passed Alignment Training" qualification
Workers will be assigned the qualification if they have accurately completed all training HITs
The alignment training HIT results .csv file will be updated with the "Approve" and "Reject columns filled out"
arg 1: alignment training HIT results (ie. Batch_[some number]_batch_results.csv)
arg 2: JSON file that stores the sets of which HITs each worker has completed
arg 3: output file that specifies which users should be granted qualification
"""

class Example:
    
# scans through each HIT (ie. row) in the .csv and checks that all answers are accurate
# if answers are accurate, the HITid will be approved and added to worker_dict
def scan_csv(batch_results, worker_dict, br_writer):
    
    print("EXAMINING HITs")
    
    line_num = 1
    approved_HITs = 0
    for row in batch_results:
        try:
            
            hitId = row[0]
            workerId = row[15]
            
            print(line_num)
            print("HIT_ID: " + hitId)
            print("Worker_ID: " + workerId)
            
            # skip first line
            if hitId == "HITId":
                continue

            # if an "unchanged" value is encountered, replace with the proper value
            if row[48] == "unchanged": #sureAlignments
                row[48] = row[31]
            if row[42] == "unchanged": #possAlignments
                row[42] = row[32]
            if row[44] == "unchanged": #sourceHighlights
                row[44] = row[33]
            if row[50] == "unchanged": #targetHighlights
                row[50] = row[34]
            
            # check if HIT is correct
            if set(row[48].split()) == set(row[35].split()) and set(row[42].split()) == set(row[36].split()) and set(row[50].split()) == set(row[38].split()) and set(row[44].split()) == set(row[37].split()):
                
                # approve HIT
                row[52] = "x"
                
                # add the HIT to the worker's set
                if workerId not in worker_dict:
                    worker_dict[workerId] = []
                worker_dict[workerId].append(hitId)
                print("HIT approved")
                approved_HITs += 1
            
            else:
                # else, reject HIT
                row[53] = "submitted alignment did not exactly match the answer key"
            
            if set(row[48].split()) != set(row[35].split()):
                print("Sure alignments incorrect, expected [" + row[35] + "], got [" + row[48] + "]")
            
            if set(row[42].split()) != set(row[36].split()):
                print("Possible alignments incorrect, expected [" + row[36] + "], got [" + row[42] + "]")
                
            if set(row[44].split()) != set(row[37].split()):
                print("Source highlights incorrect, expected [" + row[37] + "], got [" + row[44] + "]")
                
            if set(row[50].split()) != set(row[38].split()):
                print("Target highlights incorrect, expected [" + row[38] + "], got [" + row[50] + "]")
            
            # write row
            print("")
            line_num += 1
            br_writer.writerow(row)
            
        except:
            pass
    
    print("APPROVED HITS " + str(approved_HITs))
    print()
    return

# scans through the worker_dictionary and write a worker to qual_writer if they've completed all HITs
def check_workers_qualified(worker_dict, qual_writer):
    
    print("EXAMINING WORKERS")
    
    num_total_HITs = 19
    num_qualifed = 0
    
    # set of workers to delete (ie. if they have become qualified)
    delete_workers_set = sets.Set([])
    
    # write workers to qual_writer if they are qualified
    for workerId in worker_dict:
        print("WORKERID: " + workerId)
        print("NUMBER OF APPROVED HITS: " + str(len(worker_dict[workerId])))
        if len(worker_dict[workerId]) == num_total_HITs:
            qual_writer.writerow([workerId])
            delete_workers_set.add(workerId)
            num_qualifed += 1
        print("")
     
    # delete workers from worker_dict if they are qualified 
    for workerId in delete_workers_set:
        del worker_dict[workerId]
    
    
    print("NUMBER OF TOTAL WORKERS " + str(len(worker_dict)))
    print("NUMBER OF QUALIFED WORKERS: " + str(num_qualifed))
    return

def main():
    # open batch results and qualified workers .csv files
    batch_results = csv.reader(open(sys.argv[1], 'rb'), delimiter = ",")
    batch_output_name = sys.argv[1][:-4] + "_processed.csv"
    br_writer = csv.writer(open(batch_output_name, 'wb'), delimiter = ",")
    qual_writer = csv.writer(open(sys.argv[3], 'wb'), delimiter = "\t")
    
    # read in JSON data from worker_dict
    with open(sys.argv[2], 'rb') as wd_reader:
        wd_string = wd_reader.read()
    
    print(wd_string)
    worker_dict = json.loads(wd_string)
    
    # scan through each HIT result in the batch
    scan_csv(batch_results, worker_dict, br_writer)
    
    # process workers if they have become qualified
    check_workers_qualified(worker_dict, qual_writer)
    
    # dump JSON file
    with open(sys.argv[2], 'wb') as wd_writer:
        json.dump(worker_dict, wd_writer)
    
if __name__ == "__main__":
    main()

