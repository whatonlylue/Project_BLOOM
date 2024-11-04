import torch
from Bio import SeqIO


import time

records = list(SeqIO.parse("../Data/salmonella_genome_data/GCA_000006945.2/ncbi_dataset/data/GCA_000006945.2/GCA_000006945.2_ASM694v2_genomic.fna", "fasta"))

genome = records[0].seq
    
dic={"A":0.,"T":1.,"C":2.,"G":3.}



start = time.time()

#for i in range(len(genome)-3):

x = torch.tensor([[0,0,0],[1,1,1]],device='mps')
x_cat = torch.cat((x,x,x), 0)

print(x_cat.device)

#print(f"Time Elapsed: {(time.time()-start).2f}")


print(torch.backends.mps.is_available())



