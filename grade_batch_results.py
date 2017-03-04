import util_functions as util
import hits_io as brio
import hits_classes as hits

import csv

def worker_list_from_batch_results(br):
    """
    Args:
        br : the BatchResult to be processed
        
    Returns:
        A list of Workers featured in the BatchResult, with all statistics based on their 
        performance on test HITs
    """
    
    # maps name of worker -> Worker object representing the worker
    worker_dict = {}
    
    # scan through all HITTestResults in br and grade them
    for result in br.test_results:
        print "hi"
        worker_all_align = result.worker_sure_align | result.worker_poss_align
        answer_all_align = result.ans_sure_align | result.ans_poss_align
        
        # calculate precision, recall and f1 stats
        precision = util.precision(result.worker_sure_align, answer_all_align)
        recall = util.recall(worker_all_align, result.ans_sure_align)
        f1 = util.f1(precision, recall)
        
        # if worker does not exist in worker_set, add worker
        if result.worker_id not in worker_dict:
            worker = hits.Worker(
                worker_id = result.worker_id,
                total_count = 1,
                precision = None,
                recall = None,
                f1 = None
            )
            
            worker.precision = precision
            worker.recall = recall
            worker.f1 = f1
            
            worker_dict[result.worker_id] = worker
        
        # else, update the worker mapping
        else:
            worker = worker_dict[result.worker_id]
            worker.precision = (float(worker.precision * worker.total_count + precision) / 
                                (worker.total_count + 1)) 
            worker.recall = (float(worker.recall * worker.total_count + recall) / 
                                (worker.total_count + 1)) 
            worker.f1 = (float(worker.f1 * worker.total_count + f1) / 
                                (worker.total_count + 1)) 
            worker.total_count = worker.total_count + 1
    
    # return list of all workers in worker_dict
    return worker_dict.values()
        

def main():
    br = brio.csv_to_batch_results("batch_results.csv")
    print br
    l = worker_list_from_batch_results(br)
    
    workers_writer = csv.writer(open("worker_results.csv", 'wb'), delimiter = ",")
    workers_writer.writerow(["WorkerID", "# HITs completed", "Precision", "Recall", "F1"])
    
    for worker in l:
        workers_writer.writerow([worker.worker_id, worker.total_count, worker.precision, 
                                 worker.recall, worker.f1])
    
if __name__ == "__main__":
    main()