import utility


class GetFileList:
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets
        self.elem_id  = elem_id 
        self.imports  = []
    
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        dataset_lines = []
        
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
            
            if len(files) > 0:
                files = ['"' + file + '"' for file in files] 
                
                line  = '[%s]' % (",".join(files))
                dataset_lines.append(line)
            
        self.output = 'datasets%s' % str(self.elem_id)      
        
        if len(dataset_lines) > 0:  
            line = "# " + self.name
            code.append(line)
                            
            line = '%s = [%s]' % (self.output, ",".join(dataset_lines))
            code.append(line)
            
        utility.add_empty_line(code)            
        
        self.code = code
        
        
    def get_output_name(self):
        return self.output        