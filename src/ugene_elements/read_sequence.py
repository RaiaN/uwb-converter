import utility 


class ReadSequence:
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets
        self.imports  = []
        self.elem_id  = elem_id
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        self.output = "seq_records" + self.elem_id
        
        line = '%s = []' % self.output
        code.append(line)
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
                        
            if len(files) > 0:
                line = 'for filename in [%s]:' % (",".join(files)) 
                code.append(line)
                
                line = 'ftype = filename.split(".")[-1]'
                code.append(line)
                
                line = '%s += [rec for rec in SeqIO.parse(filename, ftype):' % self.output
                code.append(line)
                
                utility.add_end_indentation_line(code)
        
        self.imports.append("from Bio import SeqIO")
        
        self.code = code