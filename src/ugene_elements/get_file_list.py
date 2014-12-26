import utility


class GetFileList:
    def __init__(self, name, datasets, elem_id):
        self.name     = name
        self.datasets = datasets
        self.elem_id  = elem_id 
    
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        dataset_lines = []
        
        for dataset in datasets:
            name  = dataset[0]
            files = dataset[1] + utility.files_from_dirs(dataset[2])
            
            line  = '[%s, [%s]]' % (name, ",".join(files))
            dataset_lines.append(line)
            
        self.output = 'datasets%s' % str(self.elem_id)      
                         
        line = '%s = [%s]' % (self.output, ",".join(dataset_lines))
        code.append(line)        
        
        self.code = code
        
    def get_output_name(self):
        return self.output        