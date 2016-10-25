import csv
import sys
"""
arg 1: list of batches that should be analyzed
arg 2: worker list output of generate_worker_score_from_edinburgh
"""
def main():
    # dictionary mapping each qual type to workers of that qual type
    input_workers_dict = {"passed": [], "participated": [], "all":[]}
    output_workers_dict = {"passed": [], "participated": [], "all":[]}
    
    # open all input and output files
    list_batches = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    worker_output_stats = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
    worker_list = []
    
    # populate qual_worker_dict
    for batch in list_batches:
        qual_type = batch[0]
        if batch[0] == "passed" or batch[0] == "participated" or batch[0] == "all":
            results = csv.reader(open(batch[1], 'rU'), delimiter = ",")
            
            for row in results:
                
                worker_id = row[15]
                qual_list = input_workers_dict[qual_type]
                
                if worker_id == "WorkerId":
                    continue
                
                if worker_id not in qual_list:
                    qual_list.append(worker_id)
                    
    # print the number of workers in each
    print("input stats")
    for qual_type in input_workers_dict:
        print(qual_type + ": " + str(len(input_workers_dict[qual_type])))
    print("")
        
    # print the number of workers in each
    print("output stats")
    for qual_type in output_workers_dict:
        print(qual_type + ": " + str(len(input_workers_dict[qual_type])))
    print("")
        
    # create dictionary of workers in the output stats file
    for row in worker_output_stats:
        worker_id = row[0]
        qual_type = row[2]
        
        if qual_type == "Qualification Type":
            continue
            
        qual_list = output_workers_dict[qual_type]
            
        if worker_id not in qual_list:
            qual_list.append(worker_id)
                    
    # print out any workers who appear in input but not output
    for i in ["passed", "participated", "all"]:
        input_list = input_workers_dict[i]
        output_list = output_workers_dict[i]
        
        for worker in input_list:
            if worker not in output_list:
                print(worker + " " + i)
                
#     worker_output_stats = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
#     worker_stat_list = []
#     for row in worker_output_stats:
#         worker_stat_list.append(row[0])
#         
#     for worker in worker_list:
#         if worker not in worker_stat_list:
#             print(worker)
    
        
        

if __name__ == "__main__":
    main()
    
    