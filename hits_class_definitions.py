"""
The class definitions for HITResults and HITInput, as well as their subclasses.
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
        
    def __str__(self):
        return self.__dict__.__str__()
    
    def __repr__(self):
        return self.__str__()
    
class HITTestInput(HITInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl, ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl):
        
        HITInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                          source_hl, target_hl)
        
        self.ans_sure_align = ans_sure_align
        self.ans_poss_align = ans_poss_align
        self.ans_source_hl = ans_source_hl
        self.ans_target_hl = ans_target_hl
        
    def __str__(self):
        return self.__dict__.__str__()
        
    def __repr__(self):
        return self.__str__()
    
class HITTrainingInput(HITTestInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                     target_hl, ans_sure_align, ans_poss_align, ans_source_hl, ans_target_hl, instructions, 
                     image):
        HITTestInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                              source_hl, target_hl, ans_sure_align, ans_poss_align, ans_source_hl, 
                              ans_target_hl)
        
        self.instructions = instructions
        self.image = image
    
    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__str__()

class HITResult(HITInput):
    def __init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, source_hl, 
                 target_hl, hit_id, hit_type_id, worker_id, worker_sure_align, worker_poss_align, 
                 worker_source_hl, worker_target_hl):
        
        HITInput.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                          source_hl, target_hl)
        
        self.hit_id = hit_id
        self.hit_type_id = hit_type_id
        self.worker_id = worker_id
        self.worker_sure_align = worker_sure_align 
        self.worker_poss_align = worker_poss_align
        self.worker_source_hl = worker_source_hl
        self.worker_target_hl = worker_target_hl
        
    def __str__(self):
        return self.__dict__.__str__()
    
    def __repr__(self):
        return self.__str__()

class HITTestResult(HITResult):
    def __init__(self, pair_id = None, doc_id = None, segment_id = None, source = None, 
                 target = None, sure_align = None, poss_align = None, source_hl = None, 
                 target_hl = None,  ans_sure_align = None, ans_poss_align = None, ans_source_hl = None, 
                 ans_target_hl = None, hit_id = None, hit_type_id = None, worker_id = None, 
                 worker_sure_align = None, worker_poss_align = None, worker_source_hl = None, worker_target_hl = None, hit_result = None):
        
        if hit_result == None:
            HITResult.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                                   source_hl, target_hl, hit_id, hit_type_id, worker_id, 
                                   worker_sure_align, worker_poss_align, worker_source_hl, 
                                   worker_target_hl)
        else:
            HITResult.__init__(self, hit_result.pair_id, hit_result.doc_id, hit_result.segment_id, 
                               hit_result.source, hit_result.target, hit_result.sure_align, 
                               hit_result.poss_align, hit_result.source_hl, hit_result.target_hl, 
                               hit_result.hit_id, hit_result.hit_type_id, hit_result.worker_id, 
                               hit_result.worker_sure_align, hit_result.worker_poss_align, 
                               hit_result.worker_source_hl, hit_result.worker_target_hl)
        
        self.ans_sure_align = ans_sure_align
        self.ans_poss_align = ans_poss_align
        self.ans_source_hl = ans_source_hl
        self.ans_target_hl = ans_target_hl
    
    def __str__(self):
        return self.__dict__.__str__()
    
    def __repr__(self):
        return self.__str__()

class HITTrainingResult(HITResult):
    def __init__(self, pair_id = None, doc_id = None, segment_id = None, source = None, 
                target = None, sure_align = None, poss_align = None, source_hl = None, 
                target_hl = None, ans_sure_align = None, ans_poss_align = None, ans_source_hl = None, 
                ans_target_hl = None, instructions = None, image = None, hit_id = None, 
                hit_type_id = None, worker_id = None, worker_sure_align = None, 
                worker_poss_align = None, worker_source_hl = None, worker_target_hl = None,  
                hit_result = None):
        
        if hit_result == None:
            HITResult.__init__(self, pair_id, doc_id, segment_id, source, target, sure_align, poss_align, 
                                   source_hl, target_hl, hit_id, hit_type_id, worker_id, 
                                   worker_sure_align, worker_poss_align, worker_source_hl, 
                                   worker_target_hl)
        else:
            HITResult.__init__(self, hit_result.pair_id, hit_result.doc_id, hit_result.segment_id, 
                               hit_result.source, hit_result.target, hit_result.sure_align, 
                               hit_result.poss_align, hit_result.source_hl, hit_result.target_hl, 
                               hit_result.hit_id, hit_result.hit_type_id, hit_result.worker_id, 
                               hit_result.worker_sure_align, hit_result.worker_poss_align, 
                               hit_result.worker_source_hl, hit_result.worker_target_hl)
        
        self = hit_result
        
        self.instructions = instructions
        self.image = image
        
    def __str__(self):
        return self.__dict__.__str__()
    
    def __repr__(self):
        return self.__str__()
        
class BatchResults(object):
    def __init__(self, hit_results = [], test_results = [], training_results = []):
        self.hit_results = hit_results
        self.test_results = test_results
        self.training_results = training_results
        
    def __str__(self):
        return self.__dict__.__str__()
    
    def __repr__(self):
        return self.__str__()