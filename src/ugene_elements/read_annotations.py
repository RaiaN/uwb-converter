import utility


class ReadAnnotations:
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets
        self.imports  = []
        self.elem_id  = elem_id 
        
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)   
        
        self.output = "records" + str(self.elem_id)
        
        code = []
        ann_code = []
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
                        
            if len(files) > 0:
                line = '# ' + self.name + " " + dataset[0] 
                ann_code.append(line)
                
                files = ['"' + file + '"' for file in files] 
                
                line = 'for filename in [%s]:' % (','.join(files)) 
                ann_code.append(line)
                
                line = 'ftype = filename.split(".")[-1]'
                ann_code.append(line)
                
                line = '%s += [rec for rec in SeqIO.parse(filename, ftype)]' % self.output
                ann_code.append(line)
                
                utility.add_end_indentation_line(ann_code)
                
                utility.add_empty_line(ann_code) 
        
        if len(ann_code) > 0:
            line = '%s = []' % self.output
            code.append(line)   
            
            code += ann_code         
                
            self.imports.append("from Bio import SeqIO")
        
            utility.add_empty_line(code)
        
        self.code = code