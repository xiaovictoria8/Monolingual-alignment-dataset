import monolingual_aligner.aligner as ma

""" 
Generates a zero-indexed, Pharoah-formatted alignment string for the two input 
sentences using Sultan's monolingual aligner tool.
"""
def mono_align(src, tgt):
    alignments = ma.align(src, tgt)
    
    align_string = ""
    for align_pair in alignments[0]:
        align_string += (str((align_pair[0] - 1)) + "-" + 
                         str((align_pair[1] - 1)) + " ")
    return align_string