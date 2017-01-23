import monolingual_word_aligner.aligner as ma

def mono_align(src, tgt):
    """
    Generates a set of zero-indexed, Pharoah-formatted alignments for the two input 
    sentences using Sultan's monolingual aligner tool.
    Args:
        src : source sentence string
        tgt : target sentence string
        
    Returns:
        A set of zero-indexed, Pharoah-formatted alignments in the src and tgt strings
    """
    alignments = ma.align(src, tgt)
    
    align_set = set()
    
    for align_pair in alignments[0]:
        align_set.add(str((align_pair[0] - 1)) + "-" + 
                         str((align_pair[1] - 1)))
    return align_set
