'''Converter module'''


import re
from _collections import deque

from fetch_sequence import FetchSequence

from get_file_list import GetFileList
from read_annotations import ReadAnnotations
from read_msa import ReadMSA
from read_sequence import ReadSequence
from read_text import ReadText
from read_variations import ReadVariations

from write_annotations import WriteAnnotations
from write_fasta import WriteFasta
from write_msa import WriteMSA
from write_sequence import WriteSequence
from write_text import WriteText
from write_variations import WriteVariations
from merge_fastq import MergeFASTQ
from sequence_translation import SequenceTranslation
from reverse_complement import ReverseComplement
from dna_stats import DNAStats
from convert_alignment_to_sequence import ConvertAlignmentToSequence


# To get more information about UGENE .uwl format see
# https://ugene.unipro.ru/wiki/display/WDD15/Workflow+Designer+Manual

# To get more information about used Biopython elements see
# http://biopython.org/wiki/Category:Wiki_Documentation

class Converter(object):
    '''
    Class implements conversion of UGENE workflow to Biopython code
    See Converter.convert() for more details
    '''

    WORKFLOW = "workflow"

    GET_FILE_LIST = "get-file-list"
    READ_ANNOTATIONS = "read-annotations"
    READ_MSA = "read-msa"
    READ_SEQUENCE = "read-sequence"
    READ_TEXT = "read-text"
    READ_VARIATIONS = "read-variations"

    readers = [READ_ANNOTATIONS, READ_MSA, READ_SEQUENCE,
               READ_TEXT, READ_VARIATIONS]

    readers_dict = {GET_FILE_LIST: GetFileList,
                    READ_ANNOTATIONS: ReadAnnotations,
                    READ_MSA: ReadMSA,
                    READ_SEQUENCE: ReadSequence,
                    READ_TEXT: ReadText,
                    READ_VARIATIONS:
    ReadVariations}

    WRITE_ANNOTATIONS = "write-annotations"
    WRITE_FASTA = "write-fasta"
    WRITE_MSA = "write-msa"
    WRITE_SEQUENCE = "write-sequence"
    WRITE_VARIATIONS = "write-variations"
    WRITE_TEXT = "write-text"

    writers = [WRITE_ANNOTATIONS, WRITE_FASTA, WRITE_MSA,
               WRITE_SEQUENCE, WRITE_VARIATIONS, WRITE_TEXT]

    writers_dict = {WRITE_ANNOTATIONS: WriteAnnotations,
                    WRITE_FASTA: WriteFasta,
                    WRITE_MSA: WriteMSA,
                    WRITE_SEQUENCE: WriteSequence,
                    WRITE_VARIATIONS:
                    WriteVariations, WRITE_TEXT: WriteText}

    FETCH_SEQUENCE = "fetch-sequence"
    MERGE_FASTQ = "MergeFastq"
    SEQUENCE_TRANSLATION = "sequence-translation"
    REVERSE_COMPLEMENT = "reverse-complement"
    DNA_STATS = "dna-stats"
    CONVERT_ALN_TO_SEQ = "convert-alignment-to-sequence"

    other_dict = {FETCH_SEQUENCE: FetchSequence,
                  MERGE_FASTQ:MergeFASTQ,
                  SEQUENCE_TRANSLATION: SequenceTranslation,
                  REVERSE_COMPLEMENT: ReverseComplement,
                  DNA_STATS: DNAStats,
                  CONVERT_ALN_TO_SEQ: ConvertAlignmentToSequence}


    ALL = readers + writers + [FETCH_SEQUENCE, MERGE_FASTQ,
                               SEQUENCE_TRANSLATION, REVERSE_COMPLEMENT,
                               DNA_STATS, CONVERT_ALN_TO_SEQ]


    def __init__(self, scheme_filename):
        with open(scheme_filename) as scheme_file:
            self.scheme = scheme_file.readlines()

        self.descr = []
        self.scheme_name = ""
        self.workflow_elems = []
        self.workflow = None
        self.generated_code = None

        self.add_funcs_dict = {
            Converter.GET_FILE_LIST: self.add_reader,
            Converter.READ_ANNOTATIONS: self.add_reader,
            Converter.READ_MSA: self.add_reader,
            Converter.READ_SEQUENCE: self.add_reader,
            Converter.READ_TEXT: self.add_reader,
            Converter.READ_VARIATIONS: self.add_reader,

            Converter.WRITE_ANNOTATIONS: self.add_writer,
            Converter.WRITE_FASTA: self.add_writer,
            Converter.WRITE_MSA: self.add_writer,
            Converter.WRITE_SEQUENCE: self.add_writer,
            Converter.WRITE_VARIATIONS: self.add_writer,
            Converter.WRITE_TEXT: self.add_writer,

            Converter.FETCH_SEQUENCE: self.add_fetch_sequence,
            Converter.MERGE_FASTQ: self.add_merge_fastq,
            Converter.SEQUENCE_TRANSLATION: self.add_sequence_translation,
            Converter.REVERSE_COMPLEMENT: self.add_reverse_complement,
            Converter.DNA_STATS: self.add_dna_stats,
            Converter.CONVERT_ALN_TO_SEQ: self.add_convert_aln_to_seq
        }


    def convert(self):
        '''
        Converts scheme file into Biopython code
        '''

        self.parse_for_description()
        self.parse_for_scheme_name()
        self.parse_for_elements()
        workflow, prev_nodes = self.parse_for_workflows()
        code = self.build_biopython_workflow(workflow, prev_nodes)

        return Converter.prepare_code_as_string(code)


    def parse_for_description(self):
        '''
        Parse scheme description by Converter.WORKFLOW keyword
        '''

        ind = 0
        curr_line = self.scheme[ind].lstrip()

        while not curr_line.startswith(Converter.WORKFLOW):
            if len(self.scheme[ind].strip()) > 0:
                self.descr += [self.scheme[ind]]

            ind += 1
            curr_line = self.scheme[ind].lstrip()

        self.descr += [""]
        self.scheme = self.scheme[ind:]


    def parse_for_scheme_name(self):
        '''
        Parse scheme name
        '''

        self.scheme_name = self.scheme[0].split('"')[1]
        self.scheme = self.scheme[1:]

    def add_reader(self, ind, elem, eid, full_name):
        '''
        Parses any reader elem. Keywords: name, url-in
        '''

        datasets = []
        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')
            elif line.startswith("url-in"):
                dataset = []

                ind += 1
                line = self.scheme[ind].strip()

                while line != "}":
                    dataset.append(line)

                    ind += 1
                    line = self.scheme[ind].strip()

                datasets.append(dataset)

            ind += 1
            line = self.scheme[ind].strip()

        reader_cls = Converter.readers_dict[elem]
        w_elem = reader_cls(ename, datasets, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_writer(self, ind, elem, eid, full_name):
        '''
        Parses any writer elem. Keywords: name, url-out
        '''

        url_out = None
        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')
            elif line.startswith("url-out"):
                url_out = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        writer_cls = Converter.writers_dict[elem]
        w_elem = writer_cls(ename, url_out, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_fetch_sequence(self, ind, elem, eid, full_name):
        '''
        Parses fetch sequence elem. Keywords: name, database, resource-id
        '''

        db_name = "ncbi"  #default db
        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')
            elif line.startswith("database"):
                db_name = line.split(':')[-1].strip(';"')
            elif line.startswith("resource-id"):
                res_ids = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        elem_cls = Converter.other_dict[elem]
        w_elem = elem_cls(ename, res_ids, db_name, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_merge_fastq(self, ind, elem, eid, full_name):
        '''
        Parses merge fastq elem. Keywords: name
        '''

        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        elem_cls = Converter.other_dict[elem]
        w_elem = elem_cls(ename, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_sequence_translation(self, ind, elem, eid, full_name):
        '''
        Parses sequence translation elem. Keywords: name
        '''

        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        elem_cls = Converter.other_dict[elem]
        w_elem = elem_cls(ename, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_reverse_complement(self, ind, elem, eid, full_name):
        '''
        Parses reverse complement elem. Keywords: name
        '''

        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        elem_cls = Converter.other_dict[elem]
        w_elem = elem_cls(ename, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_dna_stats(self, ind, elem, eid, full_name):
        '''
        Parses dna stats elem. Keywords: name
        '''

        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        elem_cls = Converter.other_dict[elem]
        w_elem = elem_cls(ename, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def add_convert_aln_to_seq(self, ind, elem, eid, full_name):
        '''
        Parses convert alignment to seq elem. Keywords: name
        '''

        line = self.scheme[ind].strip()

        while line != "}":
            if line.startswith("name"):
                ename = line.split(':')[-1].strip(';"')

            ind += 1
            line = self.scheme[ind].strip()

        elem_cls = Converter.other_dict[elem]
        w_elem = elem_cls(ename, eid, full_name)
        self.workflow_elems.append(w_elem)
        eid += 1

        return ind, eid


    def try_for_element(self, ind):
        '''
        Tries to find next elem
        '''

        curr_line = self.scheme[ind]

        if curr_line.lstrip().startswith(".actor-bindings"):
            ind += 1
            return [ind, "break"]

        if "{" not in curr_line:
            ind += 1
            return [ind, "continue"]

        line = curr_line.split('{')[0].strip()
        full_name = line

        numeric = re.compile(r'[\d]+')
        line = numeric.sub('', line)
        elem = line.rstrip("-") #elem name without numbers

        if elem not in Converter.ALL:
            print("Element %s is not supported yet" % elem)
            ind += 1
            return [ind, "continue"]

        return [ind, elem, full_name]


    def parse_for_elements(self):
        '''
        General function to parse elems one by one
        '''

        ind = 0
        elem_id = 0

        while ind < len(self.scheme):
            res = self.try_for_element(ind)

            if res[1] == "break":
                break
            elif res[1] == "continue":
                ind = res[0]
                continue

            ind = res[0]
            elem = res[1]
            full_name = res[2]

            ind += 1
            elem_func = self.add_funcs_dict[elem]
            ind, elem_id = elem_func(ind, elem, elem_id, full_name)

        self.scheme = self.scheme[ind:]

    @staticmethod
    def topological_sort(adj_list):
        '''
        Determines correct order of elements in code
        '''

        order = deque()
        enter = set(i for i in range(len(adj_list)))
        visited = [False] * len(adj_list)

        def dfs(start_v):
            '''
            Runs simple DFS algorithm
            '''

            visited[start_v] = True

            for adj_v in adj_list[start_v]:
                if not visited[adj_v]:
                    enter.discard(adj_v)
                    dfs(adj_v)

            order.appendleft(start_v)

        while enter:
            dfs(enter.pop())

        return order

    def get_connections(self):
        '''
        Parses all connections in all workflows
        '''
        edges = []
        ids = {}
        nodes = {}

        ind = 0
        node_id = 0

        while ind < len(self.scheme):
            curr_line = self.scheme[ind].strip()

            if "}" in curr_line:
                break
            if "->" in curr_line:
                edge = [elem.split('.')[0] for elem in curr_line.split("->")]

                for node in edge:
                    if node not in ids.keys():
                        ids[node] = node_id
                        nodes[node_id] = node
                        node_id += 1

                edges.append(edge)

            ind += 1

        return edges, ids, nodes, node_id


    def parse_for_workflows(self):
        '''
        Parses existing workflows and represent it as directed graph
        '''

        edges, ids, nodes, nodes_count = self.get_connections()

        adj_list = [[] for i in range(nodes_count)]
        prev_nodes = {}

        for edge in edges:
            left_v = ids[edge[0]]
            right_v = ids[edge[1]]

            adj_list[left_v].append(right_v)
            prev_nodes[edge[1]] = edge[0]

        order = self.topological_sort(adj_list)

        workflow = [nodes[nid] for nid in order]

        return workflow, prev_nodes


    def build_biopython_workflow(self, workflow, prev_nodes):
        '''
        Builds workflow according to topological order
        '''

        code = ["'''"] + [self.scheme_name] + self.descr + ["'''"]

        imports = []
        body = []

        elems = self.workflow_elems
        elems_names = [elem.true_elem_name for elem in self.workflow_elems]

        first = True

        for w_elem_name in workflow:
            curr_elem = elems[elems_names.index(w_elem_name)]

            if not first and w_elem_name in prev_nodes.keys():
                prev_elem_name = prev_nodes[w_elem_name]
                prev_elem = elems[elems_names.index(prev_elem_name)]
                curr_elem.input_data = prev_elem.output

            curr_elem.generate_code()

            body += curr_elem.code
            imports += curr_elem.imports

            first = False

        code += list(set(imports)) + [""] + body

        return code


    @staticmethod
    def prepare_code_as_string(code):
        '''
        Prepares code as string
        '''

        result = ""
        indentation = 0
        four_spaces = " " * 4

        indent_prefixes = ("for ", "if ", "with ")

        for line in code:
            if line != "indentation end":
                result += four_spaces * indentation + line + "\n"
                indentation += line.startswith(indent_prefixes)
            else:
                indentation -= 1

        return result
