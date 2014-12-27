from Bio import AlignIO

records1 = []
# Чтение множественного выравнивания Dataset 1
for filename in ["/home/raian/ugene-1.14.2/data/samples/CLUSTALW/COI.aln"]:
    ftype = filename.split(".")[-1]
    records1 += [rec for rec in AlignIO.parse(filename, ftype)]


# Разделение выравнивание на последовательности
seqs0 = []
for record in records1:
    seqs0.append(record.seq)

# Запись множественного выравнивания
with open("biopython_data/outp", "w") as outp_f:
    AlignIO.write(seqs0, outp_f, "clustal")

