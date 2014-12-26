import utility

class FetchSequence: 
    dbs = {
          "ensembl": ("ensembl", ), #not supported by BioPython 
          "ncbi": ("nuccore", "gb"), 
          "ncbi-protein": ("protein", "gt"), 
          "pdb": ("pdb", ), 
          "swiss-prot": ("swiss-prot", ),
          "uniprot-swiss-prot": ("uniprot-swiss-prot", ),
          "uniprot-trembl": ("uniprot-trembl", )
          }
     
    def __init__(self, name, resource_ids, db_name):
        self.name         = name
        self.resource_ids = resource_ids.split(";")
        self.db_name      = db_name
        self.imports      = [] #need to fill it in generate_code
            
    def generate_code(self):
        code = []
        db_rettype = FetchSequence.dbs[self.db_name] 
        ids = ",".join(self.resource_ids)
        
        if db_rettype[0] == "ensembl":
            raise NotImplementedError
        elif db_rettype[0] == "nuccore" or db_rettype[0] == "protein":
            line = 'Entrez.email = "Put your email here (for Entrez)"'
            code.append(line)
            
            params = '(db="%s", id="%s", rettype="%s", retmode="text")' % (db_rettype[0], ids, db_rettype[1])
            line = 'handle = Entrez.efetch%1' % params
            code.append(line)
            
            line = 'seq_record = SeqIO.read(handle, "%s")' % db_rettype[1]
            code.append(line)    
            
            self.imports.append("from Bio import SeqIO")
            self.imports.append("from Bio import Entrez")        
        elif db_rettype[0] == "pdb":
            line = 'pdb_downloader = PDBList()'
            code.append(line)
            
            line = 'pdb_filenames = []' 
            code.append(line)
            
            line = 'for id in [%s]:' % ids
            code.append(line)                
            
            line = 'filename = pdb_downloader.retrieve_pdb_file(id)'
            code.append(line)
            
            line = 'pdb_filenames.append(filename)'
            code.append(line)
            
            utility.add_end_indentation_line(code)    
            
            self.imports.append("from Bio import PDB")
        elif db_rettype[0] == "swiss-prot":
            line = "expasy_records = []"
            code.append(line)
            
            line = 'for id in [%s]:' % ids
            code.append(line)  
            
            line = 'handle = ExPASy.get_sprot_raw(id)' 
            code.append(line)
            
            line = 'record = SwissProt.read(handle)'
            code.append(line)
            
            line = 'expasy_records.append(record)'
            code.append(line)
            
            utility.add_end_indentation_line(code)  
            
            self.imports.append("from Bio import ExPASy")
            self.imports.append("from Bio import SwissProt")
        elif db_rettype[0] == "uniprot-swiss-prot" or db_rettype[0] == "uniprot-trembl":
            line = "uniprot_records = []"
            code.append(line)
            
            line = 'for id in [%s]:' % ids
            code.append(line)  
            
            line = 'resp = requests.post("http://www.uniprot.org/uniprot/%s.txt" % id).text'
            code.append(line)
            
            line = 'uniprot_records.append(record)'
            code.append(line)
            
            line = 'time.sleep(0.3)'
            code.append(line)
            
            utility.add_end_indentation_line(code)
                      
            self.imports.append("import requests")
            self.imports.append("import time")
        else:
            raise Exception("Unknown database type")
        
        self.code = code