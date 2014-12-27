import re
from _collections import deque

from fetch_sequence import FetchSequence

from get_file_list import GetFileList
from read_annotations import ReadAnnotations
from read_msa import ReadMSA
from read_sequence import ReadSequence
from read_text import ReadText
from read_variations import ReadVariations

from write_annotations import WriteAnnotations
from write_fasta import WriteFasta
from write_msa import WriteMSA
from write_sequence import WriteSequence
from write_text import WriteText
from write_variations import WriteVariations 

from merge_fastq import MergeFASTQ 
from sequence_translation import SequenceTranslation  
from reverse_complement import ReverseComplement
from dna_stats import DNAStats
from convert_alignment_to_sequence import ConvertAlignmentToSequence 



class Converter:
    WORKFLOW = "workflow"
    
    FETCH_SEQUENCE   = "fetch-sequence"
    
    GET_FILE_LIST    = "get-file-list"
    READ_ANNOTATIONS = "read-annotations"
    READ_MSA         = "read-msa"
    READ_SEQUENCE    = "read-sequence"
    READ_TEXT        = "read-text"
    READ_VARIATIONS  = "read-variations" 
    
    readers = [READ_ANNOTATIONS, READ_MSA, READ_SEQUENCE, 
               READ_TEXT, READ_VARIATIONS]
    
    WRITE_ANNOTATIONS = "write-annotations"
    WRITE_FASTA       = "write-fasta"
    WRITE_MSA         = "write-msa"
    WRITE_SEQUENCE    = "write-sequence"
    WRITE_VARIATIONS  = "write-variations"
    WRITE_TEXT        = "write-text"
    
    MERGE_FASTQ       = "MergeFastq"
    
    SEQUENCE_TRANSLATION = "sequence-translation"
    REVERSE_COMPLEMENT   = "reverse-complement"
    DNA_STATS            = "dna-stats"
    
    CONVERT_ALIGNMENT_TO_SEQUENCE = "convert-alignment-to-sequence"
    
    writers = [WRITE_ANNOTATIONS, WRITE_FASTA, WRITE_MSA,
               WRITE_SEQUENCE, WRITE_VARIATIONS, WRITE_TEXT] 
    
    ALL = readers + writers + [FETCH_SEQUENCE, MERGE_FASTQ, 
                               SEQUENCE_TRANSLATION, REVERSE_COMPLEMENT, 
                               DNA_STATS, CONVERT_ALIGNMENT_TO_SEQUENCE] 
    
    
    def __init__(self, scheme_filename):
        with open(scheme_filename) as sf:
            self.scheme = sf.readlines()
            
                
    def convert(self):
        self.parse_for_description()
        self.parse_for_scheme_name()
        self.parse_for_elements()
        self.parse_for_workflows()
        self.build_biopython_workflow()
            
        return self.generated_code
      
      
    def parse_for_description(self):
        self.descr = []
        
        ind = 0 
        cl = self.scheme[ind].lstrip()
        
        while not cl.startswith(Converter.WORKFLOW):
            if len(self.scheme[ind].strip()) > 0:
                self.descr += [self.scheme[ind]]  
            
            ind += 1
            cl = self.scheme[ind].lstrip()
            
        self.descr += [""]    
        
        self.scheme = self.scheme[ind:]
    
    
    def parse_for_scheme_name(self):
        self.scheme_name = self.scheme[0].split('"')[1] 
        self.scheme = self.scheme[1:]       
    
    
    def parse_for_elements(self):
        ind = 0
        
        self.workflow_elems = []
        elem_id = 0
        
        while ind < len(self.scheme):
            cl = self.scheme[ind]  
            
            if cl.lstrip().startswith(".actor-bindings"):
                ind += 1               
                break
            
            if "{" not in cl:
                ind += 1
                continue
            
            line = cl.split('{')[0].strip()
            true_elem_name = line
            
            numeric = re.compile(r'[\d]+')
            line    = numeric.sub('', line)
            elem    = line.rstrip("-") #elem name without numbers
            
            if elem not in Converter.ALL:
                print("Element %s is not supported yet")
                ind += 1
                continue    
            
            ind += 1
            line = self.scheme[ind].strip()
                             
            if elem == Converter.FETCH_SEQUENCE:
                db_name = "ncbi"  #default db
                
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"')
                    elif line.startswith("database"):
                        db_name = line.split(':')[-1].strip(';"')       
                    elif line.startswith("resource-id"):
                        resource_ids = line.split(':')[-1].strip(';"')   
                        
                    ind += 1 
                    line = self.scheme[ind].strip()    
                
                fs = FetchSequence(elem_name, resource_ids, db_name, elem_id, true_elem_name)    
                
                self.workflow_elems.append(fs)     
                elem_id += 1    
                        
            elif elem in Converter.readers:
                datasets = []
                
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"') 
                    elif line.startswith("url-in"):
                        dataset = []
                        
                        ind += 1 
                        line = self.scheme[ind].strip() 
                        
                        while line != "}":
                            dataset.append(line)     
                            
                            ind += 1
                            line = self.scheme[ind].strip() 
                        
                        datasets.append(dataset) 
                        
                    ind += 1 
                    line = self.scheme[ind].strip()  
                 
                if elem == Converter.GET_FILE_LIST:
                    w_elem = GetFileList(elem_name, datasets, elem_id, true_elem_name) 
                    
                elif elem == Converter.READ_ANNOTATIONS: 
                    w_elem = ReadAnnotations(elem_name, datasets, elem_id, true_elem_name)
                    
                elif elem == Converter.READ_MSA:
                    w_elem = ReadMSA(elem_name, datasets, elem_id, true_elem_name) 
                    
                elif elem == Converter.READ_SEQUENCE:
                    w_elem = ReadSequence(elem_name, datasets, elem_id, true_elem_name)
                    
                elif elem == Converter.READ_TEXT:
                    w_elem = ReadText(elem_name, datasets, elem_id, true_elem_name)  
                    
                elif elem == Converter.READ_VARIATIONS:  
                    w_elem = ReadVariations(elem_name, datasets, elem_id, true_elem_name)  
                    
                self.workflow_elems.append(w_elem)     
                elem_id += 1      
                  
            elif elem in Converter.writers:
                url_out = None
                
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"') 
                    elif line.startswith("url-out"):
                        url_out = line.split(':')[-1].strip(';"')
                                         
                    ind += 1 
                    line = self.scheme[ind].strip()  
                    
                if elem == Converter.WRITE_ANNOTATIONS:
                    w_elem = WriteAnnotations(elem_name, url_out, elem_id, true_elem_name) 
                    
                elif elem == Converter.WRITE_FASTA: 
                    w_elem = WriteFasta(elem_name, url_out, elem_id, true_elem_name) 
                    
                elif elem == Converter.WRITE_MSA:
                    w_elem = WriteMSA(elem_name, url_out, elem_id, true_elem_name)  
                    
                elif elem == Converter.WRITE_SEQUENCE:
                    w_elem = WriteSequence(elem_name, url_out, elem_id, true_elem_name) 
                    
                elif elem == Converter.WRITE_TEXT:
                    w_elem = WriteText(elem_name, url_out, elem_id, true_elem_name)  
                    
                elif elem == Converter.WRITE_VARIATIONS:  
                    w_elem = WriteVariations(elem_name, url_out, elem_id, true_elem_name) 
                    
                self.workflow_elems.append(w_elem)     
                elem_id += 1  
                
            elif elem == Converter.MERGE_FASTQ:
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"')
                                     
                    ind += 1 
                    line = self.scheme[ind].strip()
                
                w_elem = MergeFASTQ(elem_name, elem_id, true_elem_name)
                
                self.workflow_elems.append(w_elem)     
                elem_id += 1 
                        
            elif elem == Converter.SEQUENCE_TRANSLATION:
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"')
                                     
                    ind += 1 
                    line = self.scheme[ind].strip()
                
                w_elem = SequenceTranslation(elem_name, elem_id, true_elem_name)
                 
                self.workflow_elems.append(w_elem)     
                elem_id += 1  
                
            elif elem == Converter.REVERSE_COMPLEMENT:
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"')
                                     
                    ind += 1 
                    line = self.scheme[ind].strip() 
                    
                w_elem = ReverseComplement(elem_name, elem_id, true_elem_name)
                 
                self.workflow_elems.append(w_elem)     
                elem_id += 1     
                 
            elif elem == Converter.DNA_STATS:
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"')
                                     
                    ind += 1 
                    line = self.scheme[ind].strip() 
                    
                w_elem = DNAStats(elem_name, elem_id, true_elem_name)
                 
                self.workflow_elems.append(w_elem)     
                elem_id += 1     
                  
            elif elem == Converter.CONVERT_ALIGNMENT_TO_SEQUENCE:
                while line != "}":
                    if line.startswith("name"):
                        elem_name = line.split(':')[-1].strip(';"')
                                     
                    ind += 1 
                    line = self.scheme[ind].strip() 
                    
                w_elem = ConvertAlignmentToSequence(elem_name, elem_id, true_elem_name)
                 
                self.workflow_elems.append(w_elem)     
                elem_id += 1                  
        
        self.scheme = self.scheme[ind:]
              
   
    def topological_sort(self, adj_list): # to determine correct order of elements in code
        order = deque()
        enter = set([i for i in range(len(adj_list))])
        visited = [False] * len(adj_list) 
 
        def dfs(v):
            visited[v] = True
            
            for av in adj_list[v]:
                if not visited[av]:
                    enter.discard(av)
                    dfs(av)
            
            order.appendleft(v)
 
        while enter: 
            dfs(enter.pop())
        
        return order


    def parse_for_workflows(self):
        ind = 0
        
        edges   = [] 
        ids     = {}
        nodes   = {} 
        
        node_id = 0
        
        while ind < len(self.scheme):
            cl = self.scheme[ind].strip()
            
            if "}" in cl:
                break                
        
            if "->" in cl:
                edge = [elem.split('.')[0] for elem in cl.split("->")] 
                
                for node in edge:
                    if node not in ids.keys():
                        ids[node]      = node_id
                        nodes[node_id] = node
                        node_id += 1       
                
                edges.append(edge) 
                
            ind += 1
            
        adj_list = [[] for i in range(node_id)]
        
        prev_nodes = {}
        
        for edge in edges:
            u = ids[edge[0]]
            v = ids[edge[1]]
            
            adj_list[u].append(v)    
            prev_nodes[edge[1]] = edge[0] 
             
        order = self.topological_sort(adj_list)     
            
        self.workflow   = [nodes[id] for id in order]
        self.prev_nodes = prev_nodes 
    
    
    def build_biopython_workflow(self):
        code = ["'''"] + [self.scheme_name] + self.descr + ["'''"]
        
        imports = []
        body    = []    
        
        elems = self.workflow_elems
        elems_names = [elem.true_elem_name for elem in self.workflow_elems]
        
        first = True
            
        for w_elem_name in self.workflow:
            curr_elem = elems[elems_names.index(w_elem_name)]
            
            if not first and w_elem_name in self.prev_nodes.keys():
                prev_elem_name = self.prev_nodes[w_elem_name]
                prev_elem = elems[elems_names.index(prev_elem_name)] 
                                       
                curr_elem.input_data = prev_elem.output
            
            curr_elem.generate_code()
            
            body    += curr_elem.code
            imports += curr_elem.imports
            
            first = False
         
        code += list(set(imports)) + [""] + body
              
        self.generated_code = code