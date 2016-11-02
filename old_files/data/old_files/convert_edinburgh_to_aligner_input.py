import json
import csv
import sys
import re
import sets

""" 
Takes as input a set of alignments from the Edinburgh corpus in JSON format.
Creates a CSV file of sentence pairs that will be used as input for alignment.
arg 1: Edinburgh JSON input file
arg 2: output TSV file
arg 3: 1 to generate input for berkeley aligner, any other number to generate 
       input for monolingual aligner
"""

def main():
    #open input JSON and output CSV file
    with open(sys.argv[1], 'rb') as reader:
        reader_string = reader.read()
    input = json.loads(reader_string)
    csv_writer = csv.writer(open(sys.argv[2], 'w'), delimiter = "\t")
    
    # for each sentence pair, print the source and target sentences
    for pair in input["paraphrases"]:
        try:
            pair_id = pair["id"]
            source = pair["S"]["string"]
            target = pair["T"]["string"]
            
            # output in the case of monolingual aligner
            if sys.argv[3] != "1":
                csv_writer.writerow([pair_id, source, target])
            
            # output in the case of berkeley aligner
            else:
                csv_writer.writerow([source, target])
                printed_words = sets.Set([])
                s_words = re.findall("[\w]+|[.,!?;()-]|'[\w]+", source)
                t_words = re.findall("[\w]+|[.,!?;()-]|'[\w]+", target)
                all_words = s_words + t_words
                for word in all_words:
                    if word not in printed_words:
                        csv_writer.writerow([word.lower(), word.lower()])
                        printed_words.add(word)
        
        except:
            pass
        

if __name__ == "__main__":
    main()
