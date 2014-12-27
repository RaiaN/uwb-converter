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
    
    readers_dict = {GET_FILE_LIST: GetFileList, 
                    READ_ANNOTATIONS: ReadAnnotations, READ_MSA: ReadMSA, 
                    READ_SEQUENCE: ReadSequence, READ_TEXT: ReadText,
                    READ_VARIATIONS: ReadVariations}
    
    WRITE_ANNOTATIONS = "write-annotations"
    WRITE_FASTA       = "write-fasta"
    WRITE_MSA         = "write-msa"
    WRITE_SEQUENCE    = "write-sequence"
    WRITE_VARIATIONS  = "write-variations"
    WRITE_TEXT        = "write-text"
    
    writers = [WRITE_ANNOTATIONS, WRITE_FASTA, WRITE_MSA,
               WRITE_SEQUENCE, WRITE_VARIATIONS, WRITE_TEXT] 
    
    writers_dict = {WRITE_ANNOTATIONS: WriteAnnotations, WRITE_FASTA: WriteFasta,
                    WRITE_MSA: WriteMSA, WRITE_SEQUENCE: WriteSequence, 
                    WRITE_VARIATIONS: WriteVariations, WRITE_TEXT: WriteText}
    
    MERGE_FASTQ       = "MergeFastq"
    
    SEQUENCE_TRANSLATION = "sequence-translation"
    REVERSE_COMPLEMENT   = "reverse-complement"
    DNA_STATS            = "dna-stats"
    
    CONVERT_ALIGNMENT_TO_SEQUENCE = "convert-alignment-to-sequence"
    
    
    
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
    
    
    def add_fetch_sequence(self, ind, elem_id, true_elem_name):
        db_name = "ncbi"  #default db
        
        line = self.scheme[ind].strip()
                 
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"')
            elif line.startswith("database"):
                db_name = line.split(':')[-1].strip(';"')       
            elif line.startswith("resource-id"):
                resource_ids = line.split(':')[-1].strip(';"')   
                
            ind += 1 
            line = self.scheme[ind].strip() 
            
        fs = FetchSequence(elem_name, db_name, resource_ids, elem_id, true_elem_name)    
                
        self.workflow_elems.append(fs)     
        elem_id += 1  
            
        return ind, elem_id   
    
    
    def add_reader(self, ind, elem, elem_id, true_elem_name):
        datasets = []
        
        line = self.scheme[ind].strip()
                
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
            
        reader_cls = Converter.readers_dict[elem]
        w_elem = reader_cls(elem_name, datasets, elem_id, true_elem_name) 
            
        self.workflow_elems.append(w_elem)     
        elem_id += 1           
            
        return ind, elem_id    
      
    
    def add_writer_info(self, ind, elem, elem_id, true_elem_name):
        url_out = None
        
        line = self.scheme[ind].strip()
                
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"') 
            elif line.startswith("url-out"):
                url_out = line.split(':')[-1].strip(';"')
                                 
            ind += 1 
            line = self.scheme[ind].strip()
            
        writer_cls = Converter.writers_dict[elem]
        w_elem = writer_cls(elem_name, url_out, elem_id, true_elem_name)
        
        self.workflow_elems.append(w_elem)     
        elem_id += 1  
            
        return ind, elem_id  
    
    
    def add_merge_fastq(self, ind, elem_id, true_elem_name):
        line = self.scheme[ind].strip()
        
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"')
                             
            ind += 1 
            line = self.scheme[ind].strip()
        
        w_elem = MergeFASTQ(elem_name, elem_id, true_elem_name)
        
        self.workflow_elems.append(w_elem)     
        elem_id += 1 
        
        return ind, elem_id  
    
        
    def add_sequence_translation(self, ind, elem_id, true_elem_name):
        line = self.scheme[ind].strip()
        
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"')
                             
            ind += 1 
            line = self.scheme[ind].strip()
        
        w_elem = SequenceTranslation(elem_name, elem_id, true_elem_name)
        
        self.workflow_elems.append(w_elem)     
        elem_id += 1 
        
        return ind, elem_id  
    
        
    def add_reverse_complement(self, ind, elem_id, true_elem_name):
        line = self.scheme[ind].strip()
        
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"')
                             
            ind += 1 
            line = self.scheme[ind].strip()
        
        w_elem = ReverseComplement(elem_name, elem_id, true_elem_name)
        
        self.workflow_elems.append(w_elem)     
        elem_id += 1   
        
        return ind, elem_id  
     
        
    def add_dna_stats(self, ind, elem_id, true_elem_name): 
        line = self.scheme[ind].strip()
                
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"')
                             
            ind += 1 
            line = self.scheme[ind].strip() 
            
        w_elem = DNAStats(elem_name, elem_id, true_elem_name)
         
        self.workflow_elems.append(w_elem)     
        elem_id += 1    
        
        return ind, elem_id 
    
    
    def add_convert_alignment_to_seq(self, ind, elem_id, true_elem_name):
        line = self.scheme[ind].strip()
                
        while line != "}":
            if line.startswith("name"):
                elem_name = line.split(':')[-1].strip(';"')
                             
            ind += 1 
            line = self.scheme[ind].strip() 
            
        w_elem = ConvertAlignmentToSequence(elem_name, elem_id, true_elem_name)
         
        self.workflow_elems.append(w_elem)     
        elem_id += 1    
        
        return ind, elem_id 
    
    
    def try_for_element(self, ind):
        cl = self.scheme[ind]  
        
        if cl.lstrip().startswith(".actor-bindings"):
            ind += 1               
            return [ind, "break"]
        
        if "{" not in cl:
            ind += 1
            return [ind, "continue"]
        
        line = cl.split('{')[0].strip()
        true_elem_name = line
        
        numeric = re.compile(r'[\d]+')
        line    = numeric.sub('', line)
        elem    = line.rstrip("-") #elem name without numbers
        
        if elem not in Converter.ALL:
            print("Element %s is not supported yet")
            ind += 1
            
            return [ind, "continue"]
        
        return [ind, elem, true_elem_name]   
                  
    
    def parse_for_elements(self):
        ind = 0
        elem_id = 0
        
        self.workflow_elems = []
        
        while ind < len(self.scheme):
            res = self.try_for_element(ind)
            
            if res[1] == "break":
                break
            elif res[1] == "continue":
                ind = res[0]
                continue
            
            ind            = res[0]
            elem           = res[1]
            true_elem_name = res[2]
            
            ind += 1
                             
            if elem == Converter.FETCH_SEQUENCE:
                ind, elem_id = self.add_fetch_sequence(ind, elem_id, true_elem_name)
                
            elif elem in Converter.readers:
                ind, elem_id = self.add_reader(ind, elem, elem_id, true_elem_name)
                                  
            elif elem in Converter.writers:
                ind, elem_id = self.add_writer_info(ind, elem, elem_id, true_elem_name)
                
            elif elem == Converter.MERGE_FASTQ:
                ind, elem_id = self.add_merge_fastq(ind, elem_id, true_elem_name)
                        
            elif elem == Converter.SEQUENCE_TRANSLATION:
                ind, elem_id = self.add_sequence_translation(ind, elem_id, true_elem_name)
                
            elif elem == Converter.REVERSE_COMPLEMENT:
                ind, elem_id = self.add_reverse_complement(ind, elem_id, true_elem_name)                
                 
            elif elem == Converter.DNA_STATS:
                ind, elem_id = self.add_dna_stats(ind, elem_id, true_elem_name) 
                  
            elif elem == Converter.CONVERT_ALIGNMENT_TO_SEQUENCE:
                ind, elem_id = self.add_convert_alignment_to_seq(ind, elem_id, true_elem_name)               
                
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
