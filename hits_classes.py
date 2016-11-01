"""
_the class definitions for HITResults and HITInput. 
"""

class HITInput(object):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl):
        
        self.pair_id = pair_id
        self.doc_id = doc_id
        self.segment_id = segment_id
        self.source = source
        self.target = target
        self.sure_align = sure_align
        self.poss_align = poss_align
        self.source_hl = source_hl
        self.target_hl = target_hl
    
class HITTestInput(HITInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl, ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl):
        
        HITInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                          source_hl, target_hl)
        
        self.ans_sure_align = ans_sure_align
        self.ans_poss_align = ans_poss_align
        self.ans_source_hl = ans_source_hl
        self.ans_target_hl = ans_target_hl
        
class HITTrainingInput(HITTestInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                     target_hl, ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl, instructions, 
                     image):
        HITTestInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                              source_hl, target_hl, ans_sure_align, ans_poss_align, ans_source_hl, 
                              ans_target_hl)
        self.instructions = instructions
        self.image = image

class HITResult(HITInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl, hit_id, hit_type_id, worker_id, worker_sure_align, worker_poss_align, worker_source_hl, 
                 worker_target_hl):
        
        HITInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                          source_hl, target_hl)
        
        self.hit_id = hit_id
        self.hit_type_id = hit_type_id
        self.worker_id = worker_id
        self.worker_sure_align = worker_sure_align 
        self.worker_poss_align = worker_poss_align
        self.worker_source_hl = worker_source_hl
        self.worker_target_hl = worker_target_hl

class HITTestResults(HITResult, HITTestInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl,  ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl,
                 hit_id, hit_type_id, worker_id, worker_sure_align, worker_poss_align, worker_source_hl, 
                 worker_target_hl):
        
        HITTestInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                              source_hl, target_hl, ans_sure_align, ans_poss_align, ans_source_hl, 
                              ans_target_hl)

        HITResult.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl, hit_id, hit_type_id, worker_id, worker_sure_align, worker_poss_align, worker_source_hl, 
                 worker_target_hl)

class HITTrainingResults(HITResult, HITTrainingInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                     target_hl, ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl, instructions, 
                     image, hit_id, hit_type_id, worker_id, worker_sure_align, worker_poss_align, 
                     worker_source_hl, worker_target_hl):
        
        HITTrainingInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                     target_hl, ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl, instructions, 
                     image)
        
        HITResult.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl, hit_id, hit_type_id, worker_id, worker_sure_align, worker_poss_align, worker_source_hl, 
                 worker_target_hl)
        
