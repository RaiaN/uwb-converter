from Bio import SeqIO

seq_records1 = []
# Чтение последовательности Dataset 1
for filename in ["/home/raian/ugene-1.14.2/data/samples/FASTA/human_T1.fa"]:
    ftype = filename.split(".")[-1]
    seq_records1 += [rec for rec in SeqIO.parse(filename, ftype)]


# Обратная комплементарность
reverse_complements0 = []
for record in seq_records1:
    reverse_complements0.append(record.seq.reverse_complement())

