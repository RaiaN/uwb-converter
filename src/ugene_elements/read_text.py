import utility


class ReadText:
    def __init__(self, name, datasets, elem_id, true_elem_name):
        self.name     = name
        self.datasets = datasets
        self.elem_id  = elem_id
        self.imports  = [] 
        self.true_elem_name = true_elem_name
        
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets) 
        
        self.output = "text_data" + str(self.elem_id)  
        
        code      = []
        text_code = []
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
                        
            if len(files) > 0:
                line = '# ' + self.name + " " + dataset[0] 
                text_code.append(line)
                
                files = ['"' + file + '"' for file in files]
                
                line = 'for filename in [%s]:' % (",".join(files)) 
                text_code.append(line)
                
                line = 'with open(filename, "r") as text_f:'
                text_code.append(line)
                
                line = '%s += [text_f.readlines()]' % self.output
                text_code.append(line)
                
                utility.add_end_indentation_line(text_code, count=2)
            
                utility.add_empty_line(text_code) 
        
        if len(text_code) > 0:
            line = '%s = []' % self.output
            code.append(line)
            
            code += text_code
        
            utility.add_empty_line(code)
                
        self.code = code     