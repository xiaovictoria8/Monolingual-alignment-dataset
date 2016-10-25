#!/usr/bin/python
import os
import sys
import csv
import codecs

"""
arg 1 : batch results file
arg 2 : output file
"""

def main():
    """    
    Creates a CSV file as input to the word-alignment HIT.
    """
    # read in the HIT results for the word alignment task
    csv_input_file = open(sys.argv[1])
    csv_reader = csv.reader(csv_input_file)
    csv_output_file = open(sys.argv[2], "w")
    csv_writer = csv.writer(csv_output_file)

    headers = {}
    row = csv_reader.next()
    for i, header in enumerate(row):
        headers[header] = i


    worker_counts = {}


    output_headers = ["HITId", "AssignmentId", "WorkerId", "source", "target", "gizaAlignments", "sureAlignments", "possAlignments", "sourceHighlights", "targetHighlights"]
    csv_writer.writerow(output_headers)

    for row in csv_reader:
        HITId = row[headers["HITId"]]
        AssignmentId = row[headers["AssignmentId"]]
        WorkerId = row[headers["WorkerId"]]
        source =  row[headers["Input.source"]]
        target = row[headers["Input.target"]]
        gizaAlignments = row[headers["Input.sureAlignments"]]
        sureAlignments = row[headers["Answer.sureAlignments"]]
        possAlignments = row[headers["Answer.possAlignments"]]

        # ccb - todo - these two files are mixed up for some reason that I cannot currently figure out.
        targetHighlights = row[headers["Answer.targetHighlights"]]
        sourceHighlights = row[headers["Answer.sourceHighlights"]]
        # this is my tempory hacky fix to swap the order so that they visualize properly on the 
        # grading HIT. 
        tmp = targetHighlights
        targetHighlights = sourceHighlights 
        sourceHighlights = tmp


        if not WorkerId in worker_counts:
            worker_counts[WorkerId] = 0
        worker_counts[WorkerId] += 1

        status = row[headers["AssignmentStatus"]]
#        if status != "Approved" and status != "Rejected":
        csv_writer.writerow([HITId, AssignmentId, WorkerId, source, target, gizaAlignments, sureAlignments, possAlignments, targetHighlights, sourceHighlights])



if __name__ == "__main__":
    main()



