import utility


class ReadText:
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets
        self.elem_id  = elem_id
        
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)   
        
        code = []
        
        self.output = "text_data" + self.elem_id
        
        line = '%s = []' % self.output
        code.append(line)
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
                        
            if len(files) > 0:
                line = 'for filename in [%s]:' % (",".join(files)) 
                code.append(line)
                
                line = 'with open(filename, "r") as text_f:'
                code.append(line)
                
                line = '%s += [text_f.readlines()]' % self.output
                code.append(line)
                
                utility.add_end_indentation_line(code, count=2)
                
        self.code = code     