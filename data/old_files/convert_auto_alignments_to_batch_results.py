import csv
import sys
"""
arg 1: HITs input file
"""
def main():
    #open input and output .csv files
    input_file = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    writer_name = sys.argv[1][:-4] + "_batch_results.csv"
    writer = csv.writer(open(writer_name, 'wb'), delimiter = ",")
    
    writer.writerow(["HITId","HITTypeId","Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation","AssignmentDurationInSeconds","AutoApprovalDelayInSeconds","Expiration","NumberOfSimilarHITs","LifetimeInSeconds","AssignmentId","WorkerId","AssignmentStatus","AcceptTime","SubmitTime","AutoApprovalTime","ApprovalTime","RejectionTime","RequesterFeedback","WorkTimeInSeconds","LifetimeApprovalRate","Last30DaysApprovalRate","Last7DaysApprovalRate","Input.source","Input.target","Input.docID","Input.type","Input.sureAlignments","Input.possAlignments","Input.sourceHighlights","Input.targetHighlights","Input.answerSureAlignments1","Input.answerPossAlignments1","Input.answerSourceHighlights1","Input.answerTargetHighlights1","Answer.activeTime","Answer.comment","Answer.endTime","Answer.possAlignments","Answer.sourceHighlights","Answer.startTime","Answer.submit","Answer.sureAlignments","Answer.targetHighlights","Approve","Reject"])
    
    # scan through hits input and convert each row to a "batch results" row
    for row in input_file:
        try:
            
            if row[0] == "source":
                continue
            
            batch_row = [None] * 49
            batch_row[15] = "automated aligner"
            batch_row[46] = row[4] # sure submission
            batch_row[42] = row[5] # possible submission
            batch_row[35] = row[8] # sure answers
            batch_row[36] = row[9] # target answers
        
            writer.writerow(batch_row)
        
        except:
            pass

if __name__ == "__main__":
    main()
        