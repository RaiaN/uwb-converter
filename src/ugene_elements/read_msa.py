import os
import utility

class ReadMSA:
    available_formats = ["aln", "emboss", "fasta", "ig", "nexus", "phy", "sto"]
    
    def __init__(self, name, datasets):
        self.name     = name
        self.datasets = datasets 
        
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        line = 'records = []'
        code.append(line)
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
            
            good_files = []
            
            for filename in files:  
                ftype = filename.split(".")[-1]
                
                if ftype in ReadMSA.available_formats:
                    good_files.append(filename)
                       
                        
            if len(good_files) > 0:
                line = 'for filename in [%s]:' % (",".join(good_files)) 
                code.append(line)
                
                line = 'ftype = filename.split(".")[-1]'
                code.append(line)
                
                line = 'records += [rec for rec in AlignIO.parse(filename, ftype):'
                code.append(line)
                
                utility.add_end_indentation_line(code) 