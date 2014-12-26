def prepare_datasets(datasets):   
    good_datasets = []
    
    for dataset in datasets:
        name = dataset[0].split('"')[1]
        
        files = []
        dirs  = []
        
        if len(dataset) > 1:
            for line in dataset[1:]:
                ftype, fpath = line.strip()[:-1].split(':') #remove semicolon at the end 
                if ftype == "file":
                    files.append(fpath)
                elif ftype == "dir":
                    dirs.append(fpath)
                else:
                    raise Exception("Not supported type of file")
                
        good_datasets.append([name, files, dirs]) 
        
    return good_datasets       


def add_end_indentation_line(code, count=1):  
    code += ["indentation end"] * count      