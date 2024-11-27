import torch
import warnings
import sys
from Bio import SeqIO
from transformers import AutoTokenizer
from transformers.utils import logging
import time
import os
import torch.multiprocessing as mp
from tqdm import tqdm

def parse_two_vec(genomefile: str) -> None: #Returns a tensor of ints
    """
    Parses '.fna' file using biopython and then runs it through DNABERT-2-117M to turn genome into vector
    then writes that vector to a file.

    :param genomefile: String of entire genomefile 
    """
    tokenizer = AutoTokenizer.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
      
    try:
        records = list(SeqIO.parse(f"../Data/salmonella_genome_data/{genomefile}", 'fasta'))
        genome = str(records[0].seq)
        
        inputs = tokenizer(genome, return_tensors = 'pt')['input_ids']
     
        torch.save(inputs, f'../Data/genome_vectors/{genomefile[:-4]}_tensor.pt')
    except Exception as e:
        print(f"Could not write or tokenizer: {genomefile}\nexited with error: {e}")

def get_genomefile_list() -> list[str]:
    """
    Reads all genome file names from Data/salmonella_genome_data and returns a list of them

    :returns: List of all genome files in salmonella_genome_data
    """
    
    return os.listdir("../Data/salmonella_genome_data")



def parallel_task(genomefile_list: list[str]) -> None:
    """
    Uses pytorches multiprocessing package to tokenize multiple files at once

    :param genomefile_list: List of all genomes found from Data/salmonella_genome_data

    """
    num_workers = min(9,mp.cpu_count())
    mp.set_sharing_strategy('file_system')
    mp.set_start_method('spawn')

    with mp.Pool(processes=num_workers) as pool:
        try:
            with tqdm(total=len(genomefile_list), unit='files', desc='Embedding Genomes') as pbar:
                for _ in pool.imap_unordered(parse_two_vec, genomefile_list):
                    pbar.update()
        except Exception as e:
            print(f"Error multiprocessing: {e}")

def main():
    torch.set_printoptions(threshold=2_000_000)
    if not os.path.exists("../Data/genome_vectors"):
        os.mkdir("../Data/genome_vectors")


    genomelist = get_genomefile_list()
    
    start = time.time()
    parallel_task(genomelist)
    print(f"Process Completed in {time.time()-start:.2f} seconds")

    
if __name__ == '__main__':

    logging.set_verbosity_error() 
    warnings.simplefilter('ignore',UserWarning)
    main()