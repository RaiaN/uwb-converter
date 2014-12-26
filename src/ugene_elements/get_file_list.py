import utility


class GetFileList:
    def __init__(self, name, datasets):
        self.name     = name
        self.datasets = datasets
    
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        code = []
        
        dataset_lines = []
        
        for dataset in datasets:
            name = dataset[0]
            
            files = dataset[1]
            dirs  = dataset[2]
            
            line = '[%s, [%s], [%s]]' % (name, ",".join(files), ",".join(dirs))
            dataset_lines.append(line)
                 
        
        line = 'datasets = [%s]' % (",".join(dataset_lines))
        code.append(line)
        
        self.code = code