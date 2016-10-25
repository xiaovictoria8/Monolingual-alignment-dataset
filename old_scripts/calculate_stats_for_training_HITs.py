import csv
import sys
from functions import precision, recall, f1

"""
Calculates accuracy stats regarding the the automatically generated alignments
for the training sentence pairs
arg 1: training CSV file (ie. training_HIT_new.csv)
arg 2: output CSV file
"""

def main():
    # open input and writer CSV files
    train_input = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    output_writer = csv.writer(open(sys.argv[2], 'wb'), delimiter = ",")
    
    output_writer.writerow(["hitId", "inputSureAlignments", 
                            "answerSureAlignments", "precision", "recall", 
                            "f1"])
    
    # set initial values for average precision, recall and f1
    prec_ave = -1
    rec_ave = -1
    f1_ave = -1
    
    num_hits = 0
    
    for row in train_input:
        try:
            
            if row[0] == "instructions":
                continue

            num_hits += 1
            
            # print the precision, recall and f1 performance on the current HIT
            sure_in = set(row[4].split())
            sure_ans = set(row[8].split())
            prec = precision(sure_in, sure_ans)
            rec = recall(sure_in, sure_ans)
            if prec == 0 and rec == 0:
                f1 = 0
            else:
                f1 = float(2 * prec * rec) / float(prec + rec)
            output_writer.writerow([row[0], row[4], row[8], prec, rec, f1])
            
            # set values as averages if this is the first row
            if prec_ave == -1:
                prec_ave = prec
                rec_ave = rec
                f1_ave = f1
            
            # update averages if this is not the first row
            else:
                prec_ave = float(prec_ave) + ((prec - prec_ave) / 
                                              float(num_hits))
                rec_ave = float(rec_ave) + ((rec - rec_ave) / float(num_hits))
                f1_ave = float(f1_ave) + ((f1 - f1_ave) / float(num_hits))
                
        except:
            pass
    
    # write average values
    output_writer.writerow(["average", None, None, prec_ave, rec_ave, f1_ave])
    
if __name__ == "__main__":
    main()