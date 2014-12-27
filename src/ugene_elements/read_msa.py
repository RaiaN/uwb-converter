import utility


class ReadMSA:
    available_formats = ["aln", "emboss", "fasta", "ig", "nexus", "phy", "sto"]
    
    def __init__(self, name, datasets, elem_id, true_elem_name):
        self.name     = name
        self.datasets = datasets 
        self.imports  = [] 
        self.elem_id  = elem_id 
        self.true_elem_name = true_elem_name
        
        
    def generate_code(self):
        datasets = utility.prepare_datasets(self.datasets)
        
        self.output = "records" + str(self.elem_id)
        
        code     = []
        msa_code = []
                
        for dataset in datasets:
            files = dataset[1] + utility.files_from_dirs(dataset[2])
            
            good_files = []
            
            for filename in files:  
                ftype = filename.split(".")[-1]
                
                if ftype in ReadMSA.available_formats:
                    good_files.append(filename)
                       
                        
            if len(good_files) > 0:
                line = '# ' + self.name + " " + dataset[0] 
                msa_code.append(line)
                
                good_files = ['"' + file + '"' for file in good_files] 
                
                line = 'for filename in [%s]:' % (",".join(good_files)) 
                msa_code.append(line)
                
                line = 'ftype = filename.split(".")[-1]'
                msa_code.append(line)
                
                line = '%s += [rec for rec in AlignIO.parse(filename, ftype)]' % self.output
                msa_code.append(line)
                
                utility.add_end_indentation_line(msa_code) 
                
                utility.add_empty_line(msa_code) 
                
        if len(msa_code) > 0:
            line = '%s = []' % self.output
            code.append(line)  
            
            code += msa_code       
                
                
            self.imports.append("from Bio import AlignIO")           
        
            utility.add_empty_line(code)
        
        self.code = code    