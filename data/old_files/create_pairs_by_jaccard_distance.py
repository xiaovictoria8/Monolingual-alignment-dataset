
#!/user/bin/python
import sys
import sets
import operator
import csv
import re
from functions import get_jaccard_dist

"""
Creates a CSV file that will be used as input for alignment 
Outputs the top pairs for each sentence set in the dataset, as sorted by Jaccard distance
arg 1: data (ie. all.tsv)
arg 2: CSV output file
arg 3: number of pairs to output per sentence set (ie. 1)
arg 4: 1 to output aligned word pairs (ie. as training data if you want to use berkeley aligner),
       any other number otherwise
arg 5: 1 to print the jaccard distance of each pair to stdout, any other number otherwise
"""

# returns a dictionary of the top n sentence pairs
# the dict maps (index of sentence 1, index of sentence 2) => jaccard distance
def get_top_pairs(row):
    n = int(sys.argv[3]) 
    
    jd_dict = {} # dict to be returned
                  
    # insert all viable sentence pairs into dict
    for i in range (8, len(row)):
        for j in range (i + 1, len(row)):
     
            # only select sentences that have between 5 and 30 words
            if len(row[i].split()) <= 30 and len(row[i].split()) >= 5 and len(row[j].split()) <= 30 and len(row[j].split()) >= 5:
                x = get_jaccard_dist(row[i], row[j])
                jd_dict[(i, j)] = x
    
    # get top n items
    jd_dict = sorted(jd_dict.iteritems(), key = operator.itemgetter(1), reverse = True)
    return jd_dict[:n]

def main():
    # open data files
    ldc = csv.reader(open(sys.argv[1], 'rb'), delimiter = '\t')
    csv_writer = csv.writer(open(sys.argv[2], 'w'), delimiter = "\t")
    
    for row in ldc:
        try:
            if (row[7] == "1" or row[5] == "hl"):
                continue
            
            # find top n pairs for each sentence set
            jd_dict = get_top_pairs(row)
            
            sent_num = 0;
            
            # output all items in jd_dict according to the csv format
            printed_words = sets.Set([])
            for pair in jd_dict:
                indices = pair[0]
                
                # assign an id for the sentence pair
                pair_id = row[2] + "-" + str(sent_num) 
                sent_num += 1
                
                # turn all punctuation in the sentences into a separate token
                sent0 = re.findall("[\w]+|[.,!?;()-]|'[\w]+", row[indices[0]])
                sent1 = re.findall("[\w]+|[.,!?;()-]|'[\w]+", row[indices[1]])
                
                # output the two sentences
                csv_writer.writerow([pair_id, " ".join(sent0).lower(), " ".join(sent1).lower()])

                # output single word pairs contained in the two sentences if requested
                if sys.argv[4] == "1":
                    for i in range(0, 2):
                        sent = sent0 + sent1
                        for word in sent:
                            if word not in printed_words:
                                csv_writer.writerow([word.lower(), word.lower()])
                                printed_words.add(word)

                # print jaccard distance if requested
                if sys.argv[5] == "1":
                    print(" ".join(sent0) + "\n" + " ".join(sent1) + "\n" + "Jaccard distance: " + str(pair[1]) + "\n")
        except:
             pass

if __name__ == "__main__":
    main()


