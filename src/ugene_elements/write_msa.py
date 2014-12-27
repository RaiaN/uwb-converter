import utility


class WriteMSA:
    def __init__(self, name, output_path, elem_id, true_elem_name):
        self.name = name        
        self.input_data = None
        self.output_path = output_path
        self.elem_id = elem_id
        self.output_dir = "biopython_data/"
        self.imports = []
        self.true_elem_name = true_elem_name
        
        
    def generate_code(self):
        code = []
        
        if self.input_data is None or self.output_path is None:
            self.code = code
            return
        
        line = '# ' + self.name
        code.append(line)
        
        line = 'with open("%s", "w") as outp_f:' % (self.output_dir + self.output_path)
        code.append(line)
        
        line = 'AlignIO.write(%s, outp_f, "clustal")' % (self.input_data) 
        code.append(line)
        
        utility.add_end_indentation_line(code)
        utility.add_empty_line(code)
        
        self.imports.append("from Bio import AlignIO")
                       
        self.code = code    