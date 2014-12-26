import utility


class ReadMSA:
    available_formats = ["aln", "emboss", "fasta", "ig", "nexus", "phy", "sto"]
    
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets 
        self.imports  = [] 
        self.elem_id  = elem_id 
        
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        self.output = "records" + self.elem_id
        
        line = '%s = []' % self.output
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
                
                line = '%s += [rec for rec in AlignIO.parse(filename, ftype):' % self.output
                code.append(line)
                
                utility.add_end_indentation_line(code) 
                
        self.imports.append("from Bio import AlignIO")           
        self.code = code    