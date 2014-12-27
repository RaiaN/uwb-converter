import utility


class ReadVariations:
    def __init__(self, name, datasets, elem_id):
        self.name     = name 
        self.datasets = datasets
        self.imports  = [] 
        self.elem_id  = elem_id
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code     = []
        var_code = [] 
        
        self.output = "vcf_data" + str(self.elem_id)
                
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
            
            if len(files) > 0:
                line = '# ' + self.name + " " + dataset[0] 
                var_code.append(line)
                
                files = ['"' + file + '"' for file in files]
                
                line = 'for filename in [%s]:' % files
                var_code.append(line)
                
                line = 'with open(filename, "r") as vcf_f:'
                var_code.append(line)
                
                line = 'vdata = vcf_f.readlines()'
                var_code.append(line)
                
                line = '%s.append(vdata)' % self.output 
                var_code.append(line) 
            
                utility.add_end_indentation_line(var_code, count=2)
            
                utility.add_empty_line(var_code)
                
        if len(var_code) > 0:
            line = '%s = []' % self.output
            code.append(line) 
            
            code += var_code             
        
            utility.add_empty_line(code)
        
        self.code = code