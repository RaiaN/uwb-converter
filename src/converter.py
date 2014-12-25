class Converter:
    WORKFLOW = "workflow"
    SEMICOLON = '"'
    
    def __init__(self, scheme_filename):
        with open(self.scheme_filename) as sf:
            self.scheme = sf.readlines()
            
                
    def convert(self):
        self.get_description()
        scheme_converted_str = ""
    
        return scheme_converted_str
      
      
    def parse_for_description(self):
        self.descr = ""
        
        for line_ind in range(self.scheme):
            if not self.scheme[line_ind].startswith(Converter.WORKFLOW):
                self.descr += self.scheme[line_ind]    
        
        self.scheme = self.scheme[line_ind:]
    
    
    def parse_for_scheme_name(self):
        self.scheme_name = self.scheme[0].split(Converter.SEMICOLON)[1] 
        self.scheme = self.scheme[1:]       
    
    
    def parse_for_elements(self):
        pass
    
    
    def build_biopython_workflow(self):
        pass     