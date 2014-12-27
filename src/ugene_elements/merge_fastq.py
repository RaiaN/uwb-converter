import utility


class MergeFASTQ:
    def __init__(self, name, elem_id, true_elem_name):
        self.name = name        
        self.input_data = None
        self.elem_id = elem_id
        self.output_dir = "biopython_data/"
        self.imports = []
        self.true_elem_name = true_elem_name
        
        
    def generate_code(self):
        code = []
        
        if self.input_data is None:
            self.code = code
            return
        
        line = '# ' + self.name
        code.append(line)
        
        line = 'with open("%s", "w") as outp_f:' % (self.output_dir + self.output_path + "_merged")
        code.append(line)
        
        line = 'SeqIO.write(%s, outp_f, "fastq")' % (self.input_data) 
        code.append(line)
        
        utility.add_end_indentation_line(code)
        utility.add_empty_line(code)
        
        self.imports.append("from Bio import SeqIO")
                       
        self.code = code    