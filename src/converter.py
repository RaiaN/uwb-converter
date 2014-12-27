import re
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
    
    writers = [WRITE_ANNOTATIONS, WRITE_FASTA, WRITE_MSA,
               WRITE_SEQUENCE, WRITE_VARIATIONS, WRITE_TEXT] 
    
    ALL = readers + writers + [FETCH_SEQUENCE, MERGE_FASTQ, 
                               SEQUENCE_TRANSLATION, REVERSE_COMPLEMENT] 
    
    
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
        self.descr = ""
        
        ind = 0 
        cl = self.scheme[ind].lstrip()
        
        while not cl.startswith(Converter.WORKFLOW):
            self.descr += self.scheme[ind]    
            
            ind += 1
            cl = self.scheme[ind].lstrip()
        
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
                    
                w_elem = SequenceTranslation(elem_name, elem_id, true_elem_name)
                 
                self.workflow_elems.append(w_elem)     
                elem_id += 1              
        
        self.scheme = self.scheme[ind:]
              
    
    def parse_for_workflows(self):
        ind = 0
        
        workflows = [] 
        
        while ind < len(self.scheme):
            cl = self.scheme[ind].strip()
            
            if "}" in cl:
                break                
        
            if "->" in cl:
                sequence = [elem.split('.')[0] for elem in cl.split("->")]    
                
                if len(workflows) > 0 and sequence[0] == workflows[-1][-1]:
                    workflows[-1].append(sequence[-1]) 
                else:
                    workflows.append(sequence)
                
            ind += 1
         
        self.workflows = workflows    
    
    def build_biopython_workflow(self):
        imports = []
        body    = []    
        
        all_elems = self.workflow_elems
        
        for workflow in self.workflows:
            prev_elem = None
            
            for w_elem in workflow:
                for elem in self.workflow_elems:
                    if elem.true_elem_name == w_elem:
                        if prev_elem is not None:
                            elem.input_data = prev_elem.output
                        
                        if elem in all_elems:
                            all_elems.remove(elem)
                        
                        elem.generate_code()
                        
                        body    += elem.code
                        imports += elem.imports
                        
                        prev_elem = elem
                        
                        break                 
                
        for elem in all_elems:
            elem.generate_code()
            
            body += elem.code
            imports += elem.imports 
         
        code = list(set(imports)) + [""] + body
              
        self.generated_code = code