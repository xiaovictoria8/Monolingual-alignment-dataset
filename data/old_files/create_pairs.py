"""
arg 1: data ie. all.tsv
arg 2: if for aligner then 0 else 1
"""
#!/usr/bin/python

import csv
import sys
from nltk.tokenize import wordpunct_tokenize

def main():
  ldc = csv.reader(open(sys.argv[1],'rb'), delimiter='\t')
  for row in ldc:
    try: 
      numSentences = 4
      for i in range (8, 8 + numSentences) :
        for j in range (i + 1, 8 + numSentences) :
          sent1 = wordpunct_tokenize(row[i])
          sent2 = wordpunct_tokenize(row[j])
          if len(sent1) < 50 and len(sent2) < 50:
            s1 = (" ").join(sent1)
            s2 = (" ").join(sent2)
            print s1.lower(), '\t', s2.lower()
      for i in range (8, 8 + numSentences) :
        sent = wordpunct_tokenize(row[i])
        if len(sent) < 50:
          for word in sent :
            if sys.argv[2] == 0:
              print word.lower(), '\t', word.lower()
            else:
              print word, '\t', word
    except:
            pass

if __name__ == "__main__":
    main()

