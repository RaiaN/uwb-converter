import utility

class ReadAnnotatitions:
    def __init__(self, name, datasets):
        self.name     = name
        self.datasets = datasets
        self.imports  = []
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)   
        
        code = []
        
        line = 'records = []'
        code.append(line)
        
        for dataset in datasets:
            files = dataset[1]
            dirs  = dataset[2]
                        
            if len(files) > 0:
                line = 'for filename in [%s]:' % (",".join(files)) 
                code.append(line)
                
                line = 'records += [rec for rec in SeqIO.parse(filename, "genbank"):'
                code.append(line)
                
                utility.add_end_indentation_line(code, count=1)
            
            if len(dirs) > 0: 
                line = 'for dirpath in [%s]' % dirs    
                code.append(line)
                
                line = 'files = os.listdir(dirpath)'
                code.append(line)
                
                line = 'for filename in files:'
                code.append(line)
                
                line = 'if isfile(filename):'
                code.append(line)
                
                line = 'records += [rec for rec in SeqIO.parse(filename, "genbank"):'
                code.append(line)
                
                utility.add_end_indentation_line(code, count=3)
        
        
        self.imports.append("from Bio import SeqIO")
        self.imports.append("import os")
        
        self.code = code
        
                    