import utility


class WriteSequence:
    def __init__(self, name, input_data, output_path, elem_id):
        self.name = name        
        self.input_data = input_data
        self.output_path = output_path
        self.elem_id = elem_id
        self.output_dir = "biopython_data/"
        self.imports = []
        
    def generate_code(self):
        code = []
        
        if self.input_data is None:
            self.code = code
            return
        
        line = '# ' + self.name
        code.append(line)
        
        line = 'with open(%s, "w") as outp_f:' % (self.output_dir + self.output_path)
        code.append(line)
        
        line = 'SeqIO.write(%s, outp_f, "fasta")' % (self.input_data) 
        code.append(line)
        
        utility.add_end_indentation_line(code)
        utility.add_empty_line(code)
        
        self.imports.append("from Bio import SeqIO")
                       
        self.code = code    