import sys
import csv
import random

def random_csv_embed(f1, f2, outfile):
    """
    Creates a new outfile CSV, which consists of a randomly generated merge of the items in the
    f1 and f2 CSVs.
    Note that in outfile, the order of items originally from f1 will still remain in sequential order.
    
    Args:
        f1 : The filename of the first CSV file to randomly combine
        f2 : The filename of the second CSV file to randomly combine
        outfile : The filename of the output CSV file
        
    """
    
    # read the contents of f1 and f2 into lists
    with open(f1, 'rb') as f1_o:
        f1_rd = csv.reader(f1_o, delimiter = ',', quotechar=None)
        f1_l = list(f1_rd)
        
    with open(f2, 'rb') as f2_o:
        f2_rd = csv.reader(f2_o, delimiter = ',', quotechar=None)
        f2_l = list(f2_rd)
        
    # generate a random list of line numbers in f2 that lines in f1 should be embedded after
    order_l = random.sample(range(0, len(f2_l)), len(f1_l))
    order_l.sort()
    
    # print lines from both files in merged order
    with open(outfile, 'w') as out_o:
        out_writer = csv.writer(out_o, delimiter = ',')
    
        f1_index = 0 # the line number for the next line in f1 to be printed
        order_l_index = 0
        for f2_index in f2_l:
            while order_l[order_l_index] <= f1_index:
                out_writer.write(f1_l[f1_index])
                order_l_index += 1
            
            out_writer.write(f2_l[f2_index])    

def main():
    random_csv_embed(sys.argv[0], sys.argv[1])

if __name__ == "__main__":
    main()
    