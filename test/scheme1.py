from Bio import SeqIO

seq_records0 = []
# Чтение последовательности Dataset 1
for filename in ["/home/raian/ugene-1.14.2/data/samples/FASTA/human_T1.fa"]:
    ftype = filename.split(".")[-1]
    seq_records0 += [rec for rec in SeqIO.parse(filename, ftype)]


# Аминокислотные трансляции
translated_seqs1 = []
for record in seq_records0:
    translated_seqs1.append(record.seq.translate())

# Запись последовательности
with open("biopython_data/outp", "w") as outp_f:
    SeqIO.write(translated_seqs1, outp_f, "fasta")

