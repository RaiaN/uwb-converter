import re
from fetch_sequence import FetchSequence
from get_file_list import GetFileList
from read_annotations import ReadAnnotations
from read_msa import ReadMSA
from read_sequence import ReadSequence
from read_text import ReadText
from read_variations import ReadVariations


class Converter:
    WORKFLOW = "workflow"
    
    FETCH_SEQUENCE   = "fetch-sequence"
    GET_FILE_LIST    = "get-file-list"
    READ_ANNOTATIONS = "read-annotations"
    READ_MSA         = "read-msa"
    READ_SEQUENCE    = "read-sequence"
    READ_TEXT        = "read-text"
    READ_VARIATIONS  = "read-variations" 
    
    elements = [FETCH_SEQUENCE, GET_FILE_LIST,
                READ_ANNOTATIONS, READ_MSA,
                READ_SEQUENCE, READ_TEXT, 
                READ_VARIATIONS] 
    
    def __init__(self, scheme_filename):
        with open(scheme_filename) as sf:
            self.scheme = sf.readlines()
            
                
    def convert(self):
        self.parse_for_description()
        self.parse_for_scheme_name()
        self.parse_for_elements()
        self.parse_for_workflow()
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
        elem_id        = 0
        
        while ind < len(self.scheme):
            cl   = self.scheme[ind]  
            
            if cl.lstrip().startswith(".actor-bindings"):
                self.scheme = self.scheme[ind:]
                break
            
            if "{" not in cl:
                ind += 1
                continue
            
            line = cl[:cl.index("{")].strip()
            
            numeric = re.compile(r'[\d]+')
            line    = numeric.sub('', line)
            elem    = line.rstrip("-")
            
            if elem not in Converter.elements:
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
                
                fs = FetchSequence(elem_name, resource_ids, db_name, elem_id)    
                
                self.workflow_elems.append(fs)     
                elem_id += 1    
                        
            elif elem in Converter.elements[1:]: #common for all except FETCH_SEQUENCE 
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
                    gfl = GetFileList(elem_name, datasets, elem_id)    
                    
                    self.workflow_elems.append(gfl)     
                    elem_id += 1    
                
                elif elem == Converter.READ_ANNOTATIONS: 
                    rann = ReadAnnotations(elem_name, datasets, elem_id)    
                    
                    self.workflow_elems.append(rann)     
                    elem_id += 1
                    
                elif elem == Converter.READ_MSA:
                    rmsa = ReadMSA(elem_name, datasets, elem_id)    
                    
                    self.workflow_elems.append(rmsa)     
                    elem_id += 1
                    
                elif elem == Converter.READ_SEQUENCE:
                    rseq = ReadSequence(elem_name, datasets, elem_id)    
                    
                    self.workflow_elems.append(rseq)     
                    elem_id += 1
                    
                elif elem == Converter.READ_TEXT:
                    rtext = ReadText(elem_name, datasets, elem_id)    
                    
                    self.workflow_elems.append(rtext)     
                    elem_id += 1
                    
                elif elem == Converter.READ_VARIATIONS:  
                    rvar = ReadVariations(elem_name, datasets, elem_id)    
                    
                    self.workflow_elems.append(rvar)     
                    elem_id += 1   
        
        self.scheme = self.scheme[ind:]
              
    
    def parse_for_workflow(self):
        pass
        
    
    def build_biopython_workflow(self):
        imports = []
        
        body = [] #only one import for all cases      
        
        for elem in self.workflow_elems:
            elem.generate_code()
            
            body += elem.code
            imports += elem.imports 
         
        imports = list(set(imports)) + [""]
              
        self.generated_code = imports + body