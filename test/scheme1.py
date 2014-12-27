from Bio import Entrez
from Bio import SeqIO

# Загрузить из удаленной базы данных
Entrez.email = "Put your email here (for Entrez)"
handle = Entrez.efetch(db="nuccore", id="ewqe", rettype="gb", retmode="text")
seq_record0 = SeqIO.read(handle, "gb")

# Список файлов
datasets1 = [["Dataset 1", ["/home/raian/flux/fluxgui.svg","/home/raian/flux/MANIFEST.in","/home/raian/flux/README"]]]

records2 = []
# Чтение аннотаций Dataset 1
for filename in ["/home/raian/eqwe.uwl","/home/raian/nohup.out","/home/raian/System Report.txt"]:
    ftype = filename.split(".")[-1]
    records2 += [rec for rec in SeqIO.parse(filename, ftype)]

# Чтение аннотаций Dataset 2
for filename in ["/home/raian/algo-hw-4.pdf"]:
    ftype = filename.split(".")[-1]
    records2 += [rec for rec in SeqIO.parse(filename, ftype)]


# Список файлов 1
datasets7 = [["Dataset 1", ["/home/raian/liclipse/workspace/bio_project/test/scheme1.uwl","/home/raian/liclipse/workspace/bio_project/test/scheme2.uwl"]]]

