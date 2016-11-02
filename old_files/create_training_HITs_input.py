import csv
import sys
import functions as func
import nltk
import stanford_corenlp_functions as sc_func
from progress.bar import Bar

"""
Takes in a training HITs template with instructions and source and target
sentences, produces machine alignments with Sultan's monolingual aligner.
arg 1: input HITs template
arg 2: output HITs template with machine alignments
"""

def main():
    bar = Bar('Processing', max = 52)
    
    # open input and output files
    reader = csv.reader(open(sys.argv[1], 'rb'), delimiter = ',')
    writer = csv.writer(open(sys.argv[2], 'w'), delimiter = ',')
    writer.writerow(["pairID","instructions","image","hitType","source","target",
                     "sourceLemmatized", "targetLemmatized", "jaccardDistance", 
                     "lengthDifference","sureAlignments","possAlignments",
                     "sourceHighlights","targetHighlights","answerSureAlignments",
                     "answerPossAlignments","answerSourceHighlights",
                     "answerTargetHighlights"])
    
    # find indices for important columns of input CSV
    f_row = next(reader)   
    for i in range(0, len(f_row)):
        if f_row[i] == "pairID":
            pair_i = i
        if f_row[i] == "instructions":
            inst_i = i
        if f_row[i] == "hitType":
            type_i = i
        if f_row[i] == "source":
            src_i = i
        if f_row[i] == "target":
            tgt_i = i
    
    bar.next()
            
    # for each row, find alignments and output new row
    for row in reader:
        try:
            pair_id = row[pair_i]
            inst = row[inst_i]
            stype = row[type_i]
            source = row[src_i]
            target = row[tgt_i]
            
            src_lemma = func.get_lemmatized_version(source)
            tgt_lemma = func.get_lemmatized_version(target)
            jd = func.get_jaccard_dist(src_lemma, tgt_lemma)
            ld = abs(len(nltk.word_tokenize(source)) - 
                     len(nltk.word_tokenize(target)))
            alignments = sc_func.mono_align(src_lemma, tgt_lemma)
            
            writer.writerow([pair_id, inst, "", stype, source, target, 
                             src_lemma, tgt_lemma, jd, ld, alignments, "{}", 
                             "{}", "{}", "{}", "{}", "{}", "{}"])
            
            bar.next()
        except:
            pass
    
    
if __name__ == "__main__":
    main()