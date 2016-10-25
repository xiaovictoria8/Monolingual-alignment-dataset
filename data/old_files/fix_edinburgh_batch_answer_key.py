import csv
import sys

"""
Takes as input a list of batch results for the Edinburgh HITs set.
Corrects the answer key of all batch results to match that of the HITs template input.
Also generates a batch results version of the input HITs template, 
to be processed using generate_worker_score_from_edinburgh.py

arg 1: CSV list of batch results files input
arg 2: HITs template input
"""

# create a dictionary mapping source sentence to [sure alignments, poss alignments]
def create_alignments_dict():
    template = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
    
    entry_dict = {}
    for row in template:
        try:
            print(row)
            align_list = [row[8], row [9]]
            entry_dict[row[0]] = align_list
        except:
            pass
    
    return entry_dict

# scans through every line of the input file and replaces the file's answer alignments with correct alignments
def correct_batch_results(filename, entry_dict):
    results = csv.reader(open(filename, 'rU'), delimiter = ",")
    writer_name = filename[:-4] + "_correct.csv"
    writer = csv.writer(open(writer_name, 'wb'), delimiter = ",")
    writer.writerow(["HITId","HITTypeId","Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation","AssignmentDurationInSeconds","AutoApprovalDelayInSeconds","Expiration","NumberOfSimilarHITs","LifetimeInSeconds","AssignmentId","WorkerId","AssignmentStatus","AcceptTime","SubmitTime","AutoApprovalTime","ApprovalTime","RejectionTime","RequesterFeedback","WorkTimeInSeconds","LifetimeApprovalRate","Last30DaysApprovalRate","Last7DaysApprovalRate","Input.source","Input.target","Input.docID","Input.type","Input.sureAlignments","Input.possAlignments","Input.sourceHighlights","Input.targetHighlights","Input.answerSureAlignments","Input.answerPossAlignments","Input.answerSourceHighlights","Input.answerTargetHighlights","Answer.activeTime","Answer.comment","Answer.endTime","Answer.possAlignments","Answer.sourceHighlights","Answer.startTime","Answer.submit","Answer.sureAlignments","Answer.targetHighlights","Approve","Reject"])

    # scan through the results CSV and replace answer alignments with the correct ones
    for row in results:
        try:
            # print("INITIAL ROW: " + str(row))
            align_list = entry_dict[row[27]]
            row[35] = align_list[0]
            row[36] = align_list[1]
            for i in range(39 ,48):
                # print("row " + str(i) + " has been replaced with row " + str(i+4))
                row[i] = row[i + 4]
            # print("hey")
            for i in range(48, len(row)):
                # print("row " + str(i) + " is now empty")
                row[i] = None
            # print("FINAL ROW: " + str(row))
            # print("")
            
            writer.writerow(row)
            
        except:
            pass
    
    return

def batch_results_from_template(template_filename):
    print("function starting")
    template = csv.reader(open(sys.argv[2], 'rU'), delimiter = ",")
    writer = csv.writer(open(template_filename, 'wb'), delimiter = ",")
    writer.writerow(["HITId","HITTypeId","Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation","AssignmentDurationInSeconds","AutoApprovalDelayInSeconds","Expiration","NumberOfSimilarHITs","LifetimeInSeconds","AssignmentId","WorkerId","AssignmentStatus","AcceptTime","SubmitTime","AutoApprovalTime","ApprovalTime","RejectionTime","RequesterFeedback","WorkTimeInSeconds","LifetimeApprovalRate","Last30DaysApprovalRate","Last7DaysApprovalRate","Input.source","Input.target","Input.docID","Input.type","Input.sureAlignments","Input.possAlignments","Input.sourceHighlights","Input.targetHighlights","Input.answerSureAlignments1","Input.answerPossAlignments1","Input.answerSourceHighlights1","Input.answerTargetHighlights1","Answer.activeTime","Answer.comment","Answer.endTime","Answer.possAlignments","Answer.sourceHighlights","Answer.startTime","Answer.submit","Answer.sureAlignments","Answer.targetHighlights","Approve","Reject"])
 
    print("writer initialized")
    # scan through hits input and convert each row to a "batch results" row
    for row in template:
        try:
            print("new row")
            print(row)
            if row[0] == "source":
                continue
            
            batch_row = [None] * 49
            print("INITIAL BATCH ROW: " + str(batch_row))
            batch_row[0] = "N/A"
            batch_row[30] = "test"
            batch_row[15] = "automated aligner"
            batch_row[46] = row[4] # sure submission
            batch_row[42] = row[5] # possible submission
            batch_row[35] = row[8] # sure answers
            batch_row[36] = row[9] # target answers
            print("FINAL BATCH ROW: " + str(batch_row))
        
            writer.writerow(batch_row)
        
        except:
            pass
    return

def main():
    #open input and output .csv files
    list_batches = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    
    # create dictionary mapping source sentence to alignments
    entry_dict = create_alignments_dict()
    
    # correct input batch results
    for batch in list_batches:
        if batch[1] == "filename":
            continue
        
    correct_batch_results(batch[1], entry_dict)
        
    # create batch results version of the template file
    batch_results_from_template(sys.argv[2][:-4] + "_batch_results.csv")

if __name__ == "__main__":
    main()