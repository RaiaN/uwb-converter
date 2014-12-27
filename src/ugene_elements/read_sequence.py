import utility 


class ReadSequence:
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets
        self.imports  = []
        self.elem_id  = elem_id
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
                
        self.output = "seq_records" + str(self.elem_id)
        
        code     = []
        seq_code = []
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
                        
            if len(files) > 0:
                line = '# ' + self.name + " " + dataset[0] 
                seq_code.append(line)
                
                files = ['"' + file + '"' for file in files] 
                
                line = 'for filename in [%s]:' % (",".join(files)) 
                seq_code.append(line)
                
                line = 'ftype = filename.split(".")[-1]'
                seq_code.append(line)
                
                line = '%s += [rec for rec in SeqIO.parse(filename, ftype)]' % self.output
                seq_code.append(line)
                
                utility.add_end_indentation_line(seq_code)
            
                utility.add_empty_line(seq_code) 
            
        if len(seq_code) > 0:
            line = '%s = []' % self.output
            code.append(line)    
            
            code += seq_code 
        
            self.imports.append("from Bio import SeqIO")
        
            utility.add_empty_line(code)
        
        self.code = code