import utility


class SequenceTranslation:
    def __init__(self, name, elem_id, true_elem_name):
        self.name = name        
        self.input_data = None
        self.output = None
        self.elem_id = elem_id
        self.imports = []
        self.true_elem_name = true_elem_name
        
        
    def generate_code(self):
        code = []
        
        if self.input_data is None:
            self.code = code
            return
        
        line = '# ' + self.name
        code.append(line)
        
        self.output = "translated_seqs" + str(self.elem_id)   
        
        line = '%s = []' % self.output 
        
        line = 'for record in %s' % self.input_data
        code.append(line)
        
        line = '%s.append(record.seq.translate())' % self.output
        code.append(line)
                       
        utility.add_end_indentation_line(code)
        utility.add_empty_line(code)
        
        self.imports.append("from Bio import SeqIO")
                       
        self.code = code    