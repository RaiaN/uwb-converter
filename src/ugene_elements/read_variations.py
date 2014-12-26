import utility

class ReadVariations:
    def __init__(self, name, datasets):
        self.name     = name 
        self.datasets = datasets
        self.imports  = [] 
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        line = 'vcf_data = []'
        code.append(line)
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
            
            if len(files) > 0:
                line = 'for filename in [%s]:' % files
                code.append(line)
                
                line = 'with open(filename, "r") as vcf_f:'
                code.append(line)
                
                line = 'vdata = vcf_f.readlines()'
                code.append(line)
                
                line = 'vcf_data.append(vdata)'
                code.append(line) 
            
                utility.add_end_indentation_line(code, count=2)
        
        self.code = code