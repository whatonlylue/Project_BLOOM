
import shlex
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading
import zipfile
from ncbi_scraper import run



#Checks conda env 
def is_conda_env_active():
    """Checks if conda environment 'ncbi_datasets' is active"""
    return 'CONDA_DEFAULT_ENV' in os.environ and os.environ['CONDA_DEFAULT_ENV'] == 'ncbi_datasets' 

#Creates Accesion list from salmonella_data.txt
def accesion_list_maker() -> list[str]:
    accession_list = []
    sdf = open('../Data/salmonella_data.txt','r')
    while True:
        accession = sdf.readline()

        if not accession:
            break
        else:
            accession = accession.split("%")
            if accession[2].strip() != "Null":
                accession_list.append(accession[1])
    sdf.close()
    return accession_list


#making a process to be parallelized 

def download_data_and_unzip(accession: str, index: int, retires=3) -> str:
    filename = f"{index}_salmonella_{accession}.zip"
    filepath = f"../Data/salmonella_genome_data/{filename}"

    genome_cmd = f"datasets download genome accession {accession} --filename {filename} --include genome,protein"
    genome_cmd = shlex.split(genome_cmd)
    
    for attempt in range(retires):
        res = subprocess.run(genome_cmd, cwd="../Data/salmonella_genome_data/", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            break
        time.sleep(1)
    else:
        return f"Error downloading genome {accession} after {retires} attemps"
    
    extract_path = f"../Data/salmonella_genome_data/{accession}/"
    os.makedirs(extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(filepath,'r') as zip_ref:
            
            files_to_extract = [f for f in zip_ref.namelist() if f.endswith('faa') or f.endswith('.fna')]
            zip_ref.extractall(extract_path, members=files_to_extract)

        os.remove(filepath)

        return f"Downloaded and unzipped {accession}"
    except zipfile.BadZipFile:
        return f"Failed to unzip {filename}: Bad Zip File"
    except FileNotFoundError:
        return f"File not found for removal: {filename}"



def parallelized_downloads(accession_list: list[str], start: float) -> None:
    accession_list_count = len(accession_list) - 1 
    with ThreadPoolExecutor(max_workers=(4*os.cpu_count())) as executor:
        futures = [executor.submit(download_data_and_unzip, accession, i) for i,accession in enumerate(accession_list)]
    
        for i, future in enumerate(as_completed(futures),0):
            
            with threading.Lock():
                percent = int((i / accession_list_count) * 100)
            
            dash_string = "-" * (100 - percent)
            complete_string = "#" * (percent)
            curr_time = float(time.time() - start)
        

            print(chr(27)+"[2J")
            print(f"Downloading {accession_list[i]} dataset, {i}/{accession_list_count} Time Elapsed: {curr_time:.2f} seconds")
            print(f"Process: [{complete_string + dash_string}] {percent}%")   


def main():
    if not is_conda_env_active():
        raise Exception("The conda environment 'ncbi_datasets', needs to be active to run this script")
    
    run()

    accession_list = accesion_list_maker()

    parallelized_downloads(accession_list, time.time())
    
    print("Process Completed")
    print("All genome data downloaded to Data/salmonella_genome_data")


main()
